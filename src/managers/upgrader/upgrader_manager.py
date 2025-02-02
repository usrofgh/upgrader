import asyncio

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
        self.account = AccountService(settings)
        self.accounts = self.account.accounts
        self.client = ClientService(settings)
        self.stat = StatService(len(self.accounts))
        self.promo = PromoService(settings, self.account, self.stat, self.client, self.captcha_manager)

    async def prepare_upgrader(self) -> None:
        self.client.clients = await self.client.initialize_clients(self.accounts, self.web_share.proxy_list)

    async def activate_promocodes(self) -> None:
        await self.promo.run_activation_process()

    async def get_account_balance(self, client: AsyncClient) -> dict:
        return await self.account.get_balance(client)

    async def get_all_account_balances(self) -> dict:
        tasks = []
        for client in self.client.clients:
            task = self.get_account_balance(client)
            tasks.append(task)

        balances: list[dict] = await asyncio.gather(*tasks)
        balances = {{**b} for b in balances}
        return balances
