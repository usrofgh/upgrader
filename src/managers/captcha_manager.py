import asyncio
import random
import time

from twocaptcha import TwoCaptcha


class CaptchaManager:
    def __init__(self, api_keys: list[str], proxy_list: list, site_key: str, base_url: str):
        self._solvers = [TwoCaptcha(key, proxy=proxy_list[i]) for i, key in enumerate(api_keys)]
        self.captcha_token_pool = []

        self._site_key = site_key
        self._base_url = base_url

        self._curr_solver = 0

    def solve_captcha(self) -> None:
        solver = self._solvers[self._curr_solver]
        if self._curr_solver == len(self._solvers) - 1:
            self._curr_solver = 0
        else:
            self._curr_solver += 1

        time.sleep(random.uniform(1, 3))
        code = solver.hcaptcha(sitekey=self._site_key, url=self._base_url)["code"]
        self.captcha_token_pool.append(code)
