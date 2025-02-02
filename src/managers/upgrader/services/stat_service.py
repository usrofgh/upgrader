import os

from settings import Settings

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


class StatService:
    def __init__(self, settings: Settings):
        self._settings = settings

        self.TOTAL_ACTIVATIONS = 0
        self.TOTAL_INCOME = 0.0
        self.NOT_ACTIVATED = {}
        self._curr_promo = None


    def print_stat(self) -> str:
        os.system("cls")

        stats_lines = [
            "====== STATISTIC ======\n",
            f"TOTAL ACCOUNTS: {len(self._settings.ACCOUNTS)}",
            f"TOTAL ACTIVATIONS: {self.TOTAL_ACTIVATIONS}",
            f"TOTAL INCOME: {self.TOTAL_INCOME:.2f}",
            f"TOTAL FAILED: {len(self.NOT_ACTIVATED)}",
            f"NOT ACTIVATED: {self.NOT_ACTIVATED}"
        ]
        stats_output = "\n".join(stats_lines)
        log = f"{GREEN}{stats_output}{RESET}"
        print(log)
        return log

    def reset_stat(self) -> None:
        self.TOTAL_ACTIVATIONS = 0
        self.TOTAL_INCOME = 0.0
        self.NOT_ACTIVATED = {}

    def add_error(self, email: str, msg_error: str) -> None:
        if msg_error not in self.NOT_ACTIVATED:
            self.NOT_ACTIVATED[msg_error] = [email]
        else:
            self.NOT_ACTIVATED[msg_error].append(email)
