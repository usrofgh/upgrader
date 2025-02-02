import asyncio
import base64
import datetime
import json

from httpx import AsyncClient

from settings import Settings

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://upgrader.com',
    'priority': 'u=1, i',
    'referer': 'https://upgrader.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',  # noqa
}


class ClientService:
    def __init__(self, settings: Settings):
        self.clients = []

        try:
            self._cookies = settings.upload_json(settings.COOKIES_PATH)
        except FileNotFoundError:
            self._cookies = {}

    @staticmethod
    def extract_jwt_payload(token: str) -> dict:
        payload = token.split('.')[1]

        rem = len(payload) % 4
        if rem:
            payload += '=' * (4 - rem)

        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode("utf-8")
        return json.loads(decoded_str)

    def _is_jwt_expired(self, access_token: str) -> bool:
        payload = self.extract_jwt_payload(access_token)
        exp = payload["exp"]
        now = int(datetime.datetime.now().timestamp())
        is_exp = (exp - now) < 86_000  # expired if jwt will be expired within 1 day
        return is_exp



    async def _initialize_client(self, acc: dict, proxy: str = None) -> AsyncClient:
        client = await asyncio.to_thread(AsyncClient, headers=headers, timeout=60, proxy=f"http://{proxy}")
        client.auth_data = {**acc}
        cookies = self._cookies.get(acc["email"], {})
        auth_token = cookies.get("auth")
        if cookies:
            if not self._is_jwt_expired(auth_token):
                client.headers["auth"] = cookies.pop("auth")

            for cookie in cookies:
                client.cookies.set(**cookie, domain=".upgrader.com", path="/")
        return client

    async def initialize_clients(self, accounts: list[dict], proxy_list: list[str]) -> list[AsyncClient]:
        tasks = []
        for i, acc in enumerate(accounts):
            proxy = proxy_list[i]
            task = self._initialize_client(acc, proxy)
            tasks.append(task)

        clients = await asyncio.gather(*tasks)
        return clients
