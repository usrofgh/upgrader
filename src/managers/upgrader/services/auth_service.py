import httpx
from httpx import AsyncClient

from settings import Settings


class AuthService:
    def __init__(self, settings: Settings):
        self._settings = settings


    async def login(self, client: AsyncClient) -> httpx.Response:
        # 500 {'error': True, 'msg': 'This account was not found'}
        # 200 {'error': False, 'msg': 'Logged in successfully'}

        endpoint = "https://api.upgrader.com/login/email"
        response = await client.post(endpoint, json={**client.auth_data})
        return response
