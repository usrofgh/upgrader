import asyncio

from httpx import AsyncClient
from twocaptcha import TwoCaptcha

from settings import Settings


class CaptchaManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._solver = TwoCaptcha(self._settings.TWOCAPTCHA_API)
        self._client = AsyncClient()
        self.captcha_token_pool = asyncio.Queue()

    def _solve_captcha_sync(self) -> None:
        return self._solver.hcaptcha(sitekey="a750e5fa-e446-43c0-a382-a6e055e2d76e", url="https://upgrader.com/")["code"]

    async def solve_captcha(self) -> None:
        code = await asyncio.to_thread(self._solve_captcha_sync)
        await self.captcha_token_pool.put(code)
