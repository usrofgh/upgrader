import json
import os.path
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).parent.parent.joinpath(".env"),
            Path(__file__).parent.parent.joinpath(".env.dev")
        )
    )

    LOG_LEVEL: str
    ACCOUNTS_PATH: str
    ACCOUNTS: list[dict] = []

    COOKIES_PATH: str
    COOKIES: dict[str, dict] = {}

    LOGS_PATH: str
    WEBSHARE_API: str
    TWOCAPTCHA_API: str

    PROXY_LIST: list = []


    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        self.LOGS_PATH = self.full_path(self.LOGS_PATH)
        self.ACCOUNTS_PATH = self.full_path(self.ACCOUNTS_PATH)
        self.ACCOUNTS = self.upload_json(self.full_path(self.ACCOUNTS_PATH))

        self.COOKIES_PATH = self.full_path(self.COOKIES_PATH)
        if os.path.exists(self.COOKIES_PATH):
            self.COOKIES = self.upload_json(self.COOKIES_PATH)


    @staticmethod
    def full_path(path: str) -> str:
        return str(Path(__file__).parent.joinpath(path))

    @staticmethod
    def upload_json(path: str) -> list[dict] | dict[str, dict]:
        with open(path, "r") as file:
            return json.load(file)
