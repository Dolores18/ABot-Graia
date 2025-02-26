import os

from loguru import logger
from typing import Optional
from playwright._impl._api_types import Error
from playwright.async_api import Browser, async_playwright


path_to_extension = "./util/browser/extension/ad"
user_data_dir = "./util/browser/data"


_browser: Optional[Browser] = None


async def init() -> Browser:
    global _browser
    browser = await async_playwright().start()
    _browser = await browser.chromium.launch_persistent_context(
        user_data_dir,
        headless=True,
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
        device_scale_factor=1.5,
    )
    return _browser


async def get_browser() -> Browser:
    return _browser or await init()


try:
    get_browser()
    logger.info("Chromium Browser initialized")
except Error as e:
    if str(e).startswith("Extension doesn't exist at"):
        logger.warning("未找到适应版本的 Chromium，正在自动安装...")
        os.system("playwright install chromium")
        try:
            get_browser()
        except Error as e:
            logger.error(f"Chromium 安装失败 {str(e)}，请手动执行 playwright install chromium 安装")
            exit(1)
    else:
        logger.error(f"Chromium 初始化失败 {str(e)}，未知错误")
        exit(1)
except Exception as e:
    logger.error(f"Chromium 初始化失败 {type(e)} {str(e)}，未知错误")
    exit(1)
