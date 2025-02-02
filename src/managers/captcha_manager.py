import asyncio

from httpx import AsyncClient
from twocaptcha import TwoCaptcha

from settings import Settings


class CaptchaManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._solver = TwoCaptcha(self._settings.TWOCAPTCHA_API)
        self._client = AsyncClient()
        self.captcha_token_pool = []

    def _solve_captcha_sync(self) -> None:
        code = self._solver.hcaptcha(sitekey="a750e5fa-e446-43c0-a382-a6e055e2d76e", url="https://upgrader.com/")["code"]
        self.captcha_token_pool.append(code)

    async def solve_captcha(self) -> None:
        await asyncio.to_thread(self._solve_captcha_sync)
