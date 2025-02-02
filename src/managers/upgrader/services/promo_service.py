import httpx
from httpx import AsyncClient

from settings import Settings


class PromoService:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.curr_promo = None


    async def promo_activate(self, client: AsyncClient, captcha_token: str) -> httpx.Response:
        endpoint = "https://api.upgrader.com/reward/promo/claim"
        data = {
            "promoCode": self.curr_promo,
            "token": captcha_token
        }

        response = await client.post(endpoint, json=data)
        return response


    def input_promo(self) -> None:
        self.curr_promo = input("PROMO: ")
