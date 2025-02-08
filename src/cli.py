import os

from managers.captcha_manager import CaptchaManager
from managers.upgrader.services.stat_service import GREEN, RESET
from managers.upgrader.upgrader_manager import UpgraderManager
from managers.webshare_manager import WebShareManager
from settings import Settings


class CLI:
    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    def __init__(
            self,
            settings: Settings,
            captcha_manager: CaptchaManager,
            web_share: WebShareManager,
            upgrader_manager: UpgraderManager
    ):
        self._settings = settings
        self._captcha = captcha_manager
        self._web_share = web_share
        self._upgrader_manager = upgrader_manager

    @staticmethod
    def _display_menu() -> None:
        menu = [
            "==========     MENU     ==========",
            "[1] ACTIVATE PROMO",
            "[2] ACCOUNT BALANCE",
            "[3] TOTAL BALANCE",
            "[q] STOP PROGRAM",
        ]
        msg = "\n".join(menu)
        msg = f"{GREEN}{msg}{RESET}"
        print(msg)

    def _select_option(self) -> str:
        while True:
            os.system("cls")
            self._display_menu()

            choice = input("> ").lower()
            if choice in "123q":
                return choice

    async def _activate_promocodes(self) -> None:
        await self._upgrader_manager.activate_promocodes()

    async def _get_account_balance(self) -> str:
        menu = [
            "==========     BALANCE MENU     ==========",
        ]

        for i, acc in enumerate(self._upgrader_manager.accounts):
            m = f"[{i}] {acc['email']}"
            menu.append(m)
        menu.append("\n")
        menu.append("[b] BACK")
        menu.append("[q] STOP PROGRAM")

        msg = "\n".join(menu)
        msg = f"{GREEN}{msg}{RESET}"
        print(msg)

        while True:
            n = input("> ").lower()
            if n in "bq":
                return n

            n = int(n)

            if n not in list(range(len(self._upgrader_manager.accounts))):
                continue

            client = self._upgrader_manager.client.clients[n]
            balance_info = await self._upgrader_manager.get_account_balance(client)
            for email, balance in balance_info.items():
                print(f"{email} - {balance}$")

    async def _get_total_account_balances(self) -> None:
        res = await self._upgrader_manager.get_all_account_balances()
        os.system("cls")
        menu = [
            "==========     TOTAL BALANCE     ==========",
        ]

        total_balance = 0
        i = 0
        for email, balance in res.items():
            total_balance += balance
            msg = f"{i}. {email}: {balance}"
            menu.append(msg)
            i += 1
        msg = f"\nTOTAL BALANCE: {total_balance}"

        menu.append(msg)
        msg = "\n".join(menu)
        msg = f"{GREEN}{msg}{RESET}"
        print(msg)
        print()
        print("[b] Back")
        while True:
            v = input("> ").lower()
            if v == "b":
                break

    async def run(self):
        while True:
            # choice = self._select_option().lower()
            choice = "1"
            if choice == "q":
                break

            choice_map = {
                "1": self._activate_promocodes,
                "2": self._get_account_balance,
                "3": self._get_total_account_balances,
            }
            res = await choice_map[choice]()  # noqa
            break

            if res == "q":
                break
