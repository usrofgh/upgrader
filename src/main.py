import asyncio
import sys
from pathlib import Path

from cli import CLI
from managers.captcha_manager import CaptchaManager
from managers.upgrader.upgrader_manager import UpgraderManager
from managers.webshare_manager import WebShareManager
from settings import Settings

sys.path.append(str(Path(__file__).parent))


async def main():
    settings = Settings()
    web_share = WebShareManager(webshare_api=settings.WEBSHARE_API, proxy_list_path=settings.PROXY_LIST_PATH)
    # web_share.proxy_list = web_share.get_proxy_str_list(page_size=30)

    captcha_manager = CaptchaManager(
        api_keys=settings.TWOCAPTCHA_API_KEYS,
        proxy_list=web_share.proxy_list[:len(settings.TWOCAPTCHA_API_KEYS)],
        site_key=settings.CAPTCHA_SITE_KEY,
        base_url=settings.SITE_BASE_URL
    )

    upgrader_manager = UpgraderManager(settings=settings, captcha_manager=captcha_manager, web_share_manager=web_share)
    await upgrader_manager.prepare_upgrader()

    cli = CLI(settings, captcha_manager, web_share, upgrader_manager)
    await cli.run()

if __name__ == "__main__":
    asyncio.run(main())

