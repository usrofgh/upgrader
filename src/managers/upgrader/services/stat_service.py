import os

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


class StatService:
    def __init__(self, total_accounts: int):

        self._TOTAL_ACCOUNTS = total_accounts
        self.TOTAL_ACTIVATIONS = 0
        self.TOTAL_INCOME = 0.0
        self.NOT_ACTIVATED = {}


    def print_stat(self) -> str:
        os.system("cls")
        not_activated_count = sum([len(v) for k, v in self.NOT_ACTIVATED.items()])
        stats_lines = [
            "====== STATISTIC ======\n",
            f"TOTAL ACCOUNTS: {self._TOTAL_ACCOUNTS}",
            f"TOTAL ACTIVATIONS: {self.TOTAL_ACTIVATIONS}",
            f"TOTAL INCOME: {self.TOTAL_INCOME:.2f}",
            f"TOTAL FAILED: {not_activated_count}",
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

    def update_not_activated_list(self, email: str, msg_error: str) -> None:
        if msg_error not in self.NOT_ACTIVATED:
            self.NOT_ACTIVATED[msg_error] = [email]
        else:
            self.NOT_ACTIVATED[msg_error].append(email)
