import asyncio
import random

from httpx import AsyncClient

from managers.captcha_manager import CaptchaManager
from managers.upgrader.services.account_service import AccountService
from managers.upgrader.services.client_service import ClientService
from managers.upgrader.services.promo_service import PromoService
from managers.upgrader.services.stat_service import StatService
from managers.webshare_manager import WebShareManager
from settings import Settings


class UpgraderManager:
    def __init__(
            self,
            settings: Settings,
            captcha_manager: CaptchaManager,
            web_share_manager: WebShareManager
    ):
        self.captcha_manager = captcha_manager
        self.web_share = web_share_manager
        self.client = ClientService(settings)
        self.account = AccountService(settings, self.client)
        self.accounts = self.account.accounts
        self.stat = StatService(len(self.accounts))
        self.promo = PromoService(settings, self.account, self.stat, self.client, self.captcha_manager)

    async def prepare_upgrader(self) -> None:
        self.client.clients = await self.client.initialize_clients(self.accounts, self.web_share.proxy_list)

    async def activate_promocodes(self) -> None:
        await self.promo.run_activation_process()

    async def get_account_balance(self, client: AsyncClient) -> dict:
        return await self.account.get_balance(client)

    async def _get_account_balance_delay(self, client: AsyncClient) -> dict:
        await asyncio.sleep(random.uniform(1, 3))
        return await self.account.get_balance(client)

    async def get_all_account_balances(self) -> dict:
        tasks = []
        for client in self.client.clients:
            task = self._get_account_balance_delay(client)
            tasks.append(task)

        balance_data: list[dict] = await asyncio.gather(*tasks)
        res = {}
        for el in balance_data:
            res.update(el)
        return res
