import httpx


class WebShareManager:
    def __init__(self, webshare_api: str, proxy_list_path: str) -> None:
        self._webshare_api = webshare_api
        self.proxy_list = self._upload_proxy_list(proxy_list_path)


    @staticmethod
    def _upload_proxy_list(path: str) -> list[str]:
        with open(path, "r") as file:
            proxy_list = [line.strip() for line in file.readlines()]
            return proxy_list

    def get_proxy_list(self, page_size: int) -> dict:
        endpoint = "https://proxy.webshare.io/api/v2/proxy/list/"
        headers = {"Authorization": self._webshare_api}
        params = {"mode": "direct", "page": 1, "page_size": page_size}
        response = httpx.get(endpoint, headers=headers, params=params)
        return response.json()

    def get_proxy_str_list(self, page_size: int) -> list[str]:
        proxies = self.get_proxy_list(page_size)
        proxy_strs = [f"{p['proxy_address']}:{p['port']}" for p in proxies["results"]]
        return proxy_strs
