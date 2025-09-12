import os
import time

from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Locators:
    """Locators for the Navigation page."""
    APP_USE_POPUP = (By.XPATH, "//*[contains(text(), 'Open') and contains(text(), 'App')]")

class Navigation(BasePage):
    """
    Class for navigating the Twitch website.
    """
    def __init__(self, driver) -> None:
        """
        Initialize the Navigation page object.
        """
        super().__init__(driver)
        self.driver = driver

    def open_base_page(self) -> None:
        """
        Open the base URL from environment variables.        """
        base_url = os.getenv(key='UI_URL')
        self.driver.get(base_url)

    def scroll_bottom_of_page(self, times_to_scroll: int = 1) -> None:
        """
        Scroll to the bottom of the page a specified number of times.

        :param times_to_scroll: int, number of times to scroll to the bottom.
        """
        for _ in range(times_to_scroll):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)

    def scroll_top_of_page(self) -> None:
        """
        Scroll to the top of the page.
        """
        self.driver.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

    def clear_popup_windows(self) -> None:
        """
        Handle the sign-in popup if it appears.
        """
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()

    def locate_and_close_app_use_popup(self, timeout: int = 5) -> None:
        """
        Locate and close the app uses popup if it appears.
        """
        self.explicit_wait(5)
        try:
            popup = self.get_present_element(Locators.APP_USE_POPUP, timeout=timeout)
            if popup.is_displayed():
                self.clear_popup_windows()
        except Exception:
            pass
