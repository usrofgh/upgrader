import asyncio
import threading

import httpx
from httpx import AsyncClient

from managers.captcha_manager import CaptchaManager
from managers.upgrader.services.account_service import AccountService
from managers.upgrader.services.client_service import ClientService
from managers.upgrader.services.stat_service import StatService
from settings import Settings


class PromoService:
    def __init__(
            self,
            settings: Settings,
            account: AccountService,
            stat: StatService,
            client: ClientService,
            captcha: CaptchaManager,
    ):
        self._settings = settings
        self._account = account
        self._stat = stat
        self._client = client
        self._captcha = captcha
        self.curr_promo = None

    async def _activate_promo(self, client: AsyncClient, captcha_token: str) -> httpx.Response:
        endpoint = "https://api.upgrader.com/reward/promo/claim"
        data = {
            "promoCode": self.curr_promo,
            "token": captcha_token
        }

        response = await client.post(endpoint, json=data)
        return response


    async def _flow(self, client: AsyncClient) -> None:
        self._stat.print_stat()
        email = client.auth_data["email"]
        if "auth" not in client.headers:
            response = await self._account.login(client)
            resp_data = response.json()
            if resp_data.get("error"):
                self._stat.update_not_activated_list(email, resp_data["msg"])
                self._stat.print_stat()
                return
            else:
                self._client.update_cookies(email, dict(client.cookies))

        while True:
            if not self._captcha.captcha_token_pool:
                await asyncio.sleep(1)
                continue

            token = self._captcha.captcha_token_pool.pop(0)
            response = await self._activate_promo(client, token)
            if response.status_code == 401:
                await self._account.login(client)
                self._client.update_cookies(email, dict(client.cookies))
                await asyncio.sleep(1)
                continue

            resp_data = response.json()
            if resp_data.get("error"):
                self._stat.update_not_activated_list(client.auth_data["email"], resp_data["msg"])
                self._stat.print_stat()
            else:
                income = resp_data["msg"].split("$")[-1].strip()
                self._stat.TOTAL_ACTIVATIONS += 1
                self._stat.TOTAL_INCOME += float(income)
                self._stat.print_stat()

            break


        cookies = dict(client.cookies)
        self._client._cookies[client.auth_data["email"]] = cookies

    def _solve_captcha(self) -> None:
        self._captcha.solve_captcha()

    async def run_activation_process(self) -> None:
        for _ in range(len(self._client.clients) * 2):
            thread = threading.Thread(target=self._solve_captcha)
            thread.start()


        self.curr_promo = input("PROMO: ")
        self._stat.reset_stat()
        await asyncio.gather(*[self._flow(c) for c in self._client.clients])

        with open(self._settings.LOGS_PATH, "a") as file:
            log = self._stat.print_stat() + "\n\n"
            file.write(log)

        input("ENTER ANY LETTER TO STOP: ")
