import asyncio
import random

from twocaptcha import TwoCaptcha


class CaptchaManager:
    def __init__(self, api_keys: list[str], proxy_list: list, site_key: str, base_url: str):
        self._solvers = [TwoCaptcha(key, proxy=proxy_list[i]) for i, key in enumerate(api_keys)]
        self.captcha_token_pool = []

        self._site_key = site_key
        self._base_url = base_url

        self._curr_solver = 0

    def _solve_captcha_sync(self) -> None:
        solver = self._solvers[self._curr_solver]
        if self._curr_solver == len(self._solvers) - 1:
            self._curr_solver = 0
        else:
            self._curr_solver += 1

        return solver.hcaptcha(sitekey=self._site_key, url=self._base_url)["code"]

    async def solve_captcha(self) -> None:
        await asyncio.sleep(random.uniform(0, 2))
        code = await asyncio.to_thread(self._solve_captcha_sync)
        self.captcha_token_pool.append(code)
