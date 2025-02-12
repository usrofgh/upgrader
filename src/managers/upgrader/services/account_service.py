from httpx import AsyncClient, Response

from managers.upgrader.services.client_service import ClientService
from settings import Settings


class AccountService:
    def __init__(self, settings: Settings, client_service: ClientService):
        self._settings = settings
        self.accounts = self._settings.upload_json(self._settings.ACCOUNTS_PATH)
        self._client_service = client_service

    async def get_balance(self, client: AsyncClient) -> dict:
        endpoint = "https://api.upgrader.com/user/balance"
        response = await client.get(endpoint)
        if response.status_code == 401:
            await self.login(client)
            self._client_service.update_cookies(client.auth_data["email"], dict(client.cookies))
            response = await client.get(endpoint)
        data = response.json()
        balance = float(data["data"]["balance"]) / 100
        res = {client.auth_data["email"]: balance}
        return res

    @staticmethod
    async def login(client: AsyncClient) -> Response:
        # 500 {'error': True, 'msg': 'This account was not found'}
        # 200 {'error': False, 'msg': 'Logged in successfully'}

        endpoint = "https://api.upgrader.com/login/email"
        response = await client.post(endpoint, json={**client.auth_data})
        return response
