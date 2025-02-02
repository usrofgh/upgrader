import asyncio
import json

from httpx import AsyncClient

from managers.captcha_manager import CaptchaManager
from managers.upgrader.services.auth_service import AuthService
from managers.upgrader.services.client_service import ClientService
from managers.upgrader.services.promo_service import PromoService
from managers.upgrader.services.stat_service import StatService
from settings import Settings


class UpgraderManager:
    def __init__(self, settings: Settings, captcha_manager: CaptchaManager):
        self._settings = settings
        self._auth = AuthService(settings)
        self._promo = PromoService(settings)
        self._stat = StatService(settings)
        self._client = ClientService(settings)
        self._captcha_manager = captcha_manager


    async def _flow(self, client: AsyncClient) -> None:
        self._stat.print_stat()
        if "auth" not in client.headers:
            response = await self._auth.login(client)
            resp_data = response.json()
            if resp_data.get("error"):
                self._stat.add_error(client.auth_data["email"], resp_data["msg"])
                self._stat.print_stat()
                return

        while True:
            if self._captcha_manager.captcha_token_pool:
                token = self._captcha_manager.captcha_token_pool.pop(0)
                response = await self._promo.promo_activate(client, token)
                if response.status_code == 401:
                    await self._auth.login(client)
                    continue

                resp_data = response.json()
                if resp_data.get("error"):
                    self._stat.add_error(client.auth_data["email"], resp_data["msg"])
                    self._stat.print_stat()
                else:
                    income = resp_data["msg"].split("$")[-1].strip()
                    self._stat.TOTAL_ACTIVATIONS += 1
                    self._stat.TOTAL_INCOME += float(income)
                    self._stat.print_stat()

                break
            await asyncio.sleep(1)

        cookies = dict(client.cookies)
        self._settings.COOKIES[client.auth_data["email"]] = cookies

    async def run_activation_process(self) -> None:
        print("==========     START     ==========")

        clients = await self._client.initialize_clients()
        self._stat.reset_stat()
        self._promo.input_promo()
        self._stat.curr_promo = self._promo.curr_promo
        await asyncio.gather(*[self._flow(c) for c in clients])

        with open(self._settings.LOGS_PATH, "a") as file:
            log = self._stat.print_stat() + "\n\n"
            file.write(log)

        with open(self._settings.COOKIES_PATH, "w") as file:
            json.dump(self._settings.COOKIES, file, indent=4)

        input("ENTER ANY LETTER TO STOP: ")
