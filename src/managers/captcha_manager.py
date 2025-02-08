import random
import threading
import time
from datetime import datetime, timedelta

from twocaptcha import TwoCaptcha


class CaptchaManager:
    def __init__(self, api_keys: list[str], proxy_list: list, site_key: str, base_url: str):
        self._solvers = [TwoCaptcha(key, proxy=proxy_list[i]) for i, key in enumerate(api_keys)]
        self.captcha_token_pool = []
        self._count_solving = 0

        self._site_key = site_key
        self._base_url = base_url

        self._curr_solver = 0

    def solve_captcha(self) -> None:
        solver = self._solvers[self._curr_solver]
        if self._curr_solver == len(self._solvers) - 1:
            self._curr_solver = 0
        else:
            self._curr_solver += 1

        time.sleep(random.uniform(0, 3))
        try:
            code = solver.hcaptcha(sitekey=self._site_key, url=self._base_url)["code"]
        except Exception:
            return


        captcha_ttl = 120
        solver_delay = 5
        next_solver_run = 30
        actual_ttl = captcha_ttl - solver_delay - next_solver_run
        expire_at = datetime.now() + timedelta(seconds=actual_ttl)
        self.captcha_token_pool.append({"expiry": expire_at, "code": code, "is_replaced": False})

    def keep_tokens_fresh(self) -> None:
        i = 0
        while True:
            if not self.captcha_token_pool:
                continue

            expiry = self.captcha_token_pool[i]["expiry"]
            now = datetime.now()
            is_replaced = self.captcha_token_pool[i]["is_replaced"]
            if now >= expiry and is_replaced is False:
                threading.Thread(target=self.solve_captcha).start()
                self.captcha_token_pool[i]["is_replaced"] = True
                is_replaced = True

            if (now - expiry).total_seconds() > 20 and is_replaced:
                self.captcha_token_pool.pop(i)
            else:
                i += 1

            if i >= len(self.captcha_token_pool):
                print(len(self.captcha_token_pool))
                time.sleep(1)
                i = 0

    def extract_oldest_token(self) -> str:
        token = sorted(self.captcha_token_pool, key=lambda x: x["expiry"])[0]
        self.captcha_token_pool.remove(token)
        return token["code"]
