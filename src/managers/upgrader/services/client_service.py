import asyncio

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
        self._settings = settings

    async def _initialize_client(self, acc: dict, proxy: str = None) -> AsyncClient:
        client = await asyncio.to_thread(AsyncClient, headers=headers, timeout=60, proxy=f"http://{proxy}")
        client.auth_data = {**acc}
        cookies = self._settings.COOKIES.get(acc["email"], {})
        if cookies:
            client.headers["auth"] = cookies.pop("auth")
            for cookie in cookies:
                client.cookies.set(**cookie, domain=".upgrader.com", path="/")
        return client

    async def initialize_clients(self) -> list[AsyncClient]:
        tasks = []
        for i, acc in enumerate(self._settings.ACCOUNTS):
            proxy = self._settings.PROXY_LIST[i]
            task = self._initialize_client(acc, proxy)
            tasks.append(task)

        clients = await asyncio.gather(*tasks)
        return clients
