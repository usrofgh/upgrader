from httpx import AsyncClient

from settings import Settings


class AuthService:
    def __init__(self, settings: Settings):
        self._settings = settings


    async def login(self, client: AsyncClient) -> bool:
        # 500 {'error': True, 'msg': 'This account was not found'}
        # 200 {'error': False, 'msg': 'Logged in successfully'}

        endpoint = "https://api.upgrader.com/login/email"
        response = await client.post(endpoint, json={**client.auth_data})
        resp_data = response.json()
        if resp_data.get("error"):
            self.add_error(client.auth_data["email"], resp_data["msg"])
            self.print_stat()
            return False
        return True
