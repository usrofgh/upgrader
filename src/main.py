import asyncio
import sys
from pathlib import Path

from managers.captcha_manager import CaptchaManager
from managers.upgrader.upgrader_manager import UpgraderManager
from managers.webshare_manager import WebShareManager
from settings import Settings

sys.path.append(str(Path(__file__).parent))


async def main():
    settings = Settings()
    captcha_manager = CaptchaManager(settings=settings)

    web_share = WebShareManager(settings=settings)
    upgrader_manager = UpgraderManager(settings=settings, captcha_manager=captcha_manager)

    count_accounts = len(settings.ACCOUNTS)
    settings.PROXY_LIST = web_share.get_proxy_str_list(page_size=count_accounts)

    for _ in range(count_accounts):
        asyncio.create_task(captcha_manager.solve_captcha())

    await upgrader_manager.run_activation_process()

if __name__ == "__main__":
    asyncio.run(main())
