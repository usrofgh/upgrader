import httpx

from settings import Settings


class WebShareManager:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_proxy_list(self, page_size: int) -> dict:
        endpoint = "https://proxy.webshare.io/api/v2/proxy/list/"
        headers = {"Authorization": self._settings.WEBSHARE_API}
        params = {"mode": "direct", "page": 1, "page_size": page_size}
        response = httpx.get(endpoint, headers=headers, params=params)
        return response.json()

    def get_proxy_str_list(self, page_size: int) -> list[str]:
        proxies = self.get_proxy_list(page_size)
        proxy_strs = [f"{p['proxy_address']}:{p['port']}" for p in proxies["results"]]
        return proxy_strs
