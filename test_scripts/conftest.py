import os
import os.path
import stat
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from main_api import Api
from main_ui import Ui


@pytest.fixture(scope="function", name='api')
def tf_api() -> Generator[Api, None, None]:
    """
    Fixture to provide an Api instance for tests.

    :return: Generator yielding an Api instance
    """
    api_base_url = os.getenv(key='API_URL')
    api_access_key = os.getenv(key='API_ACCESS_KEY')
    yield Api(api_base_url, api_access_key)

@pytest.fixture(scope="function", name="ui")
def tf_ui() -> Generator[Ui, None, None]:
    """
    Fixture to provide an Ui instance for tests.

    :return: Generator yielding an Ui instance
    """
    driver_options = webdriver.ChromeOptions()

    driver_options.add_argument("--headless=new")
    mobile_emulation = {"deviceName": "Pixel 2"}
    driver_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver_path = ChromeDriverManager().install()

    if driver_path and os.name != "nt":
        st = os.stat(driver_path)
        os.chmod(driver_path, st.st_mode | stat.S_IEXEC)

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=driver_options,
    )

    driver.implicitly_wait(10)
    ui = Ui(driver)

    try:
        yield ui
    finally:
        ui.browse_page.take_screenshot(os.path.join(os.path.dirname(__file__), 'test_data', 'screenshots', 'screenshot.png'))
        try:
            driver.close()
        except WebDriverException as exc:
            print(f"Exception during driver close: {exc}")
        try:
            driver.quit()
        except WebDriverException as exc:
            print(f"Exception during driver quit: {exc}")
