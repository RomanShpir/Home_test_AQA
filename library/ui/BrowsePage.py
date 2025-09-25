import random

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from library.ui.BasePage import BasePage


class Locators:
    """Locators for the Browse page."""

    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    CATEGORY_LINK = (By.XPATH, "//p[@title='{}']")
    STREAM_LIST = (By.XPATH, "//div[contains(@class,'Layout-sc-')]//article")


class BrowsePage(BasePage):
    """
    Page object for the Browse page.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def input_search_category_name(self, category_name: str) -> None:
        """
        Input the category name into the search field.

        :param category_name: str, the name of the category to search for.
        :raise: NoSuchElementException
        """
        search_field = self.get_clickable_element(Locators.SEARCH_INPUT)
        search_field.clear()
        search_field.send_keys(category_name)
        self.wait_dome_to_load()

    def select_category_from_search_results(self, category_name: str) -> None:
        """
        Select a category from the search results by its name.

        :param category_name: str, the name of the category to select.
        :raise: NoSuchElementException
        """
        xpath = self._format_tuple(Locators.CATEGORY_LINK, category_name)
        self.get_clickable_element(xpath).click()
        self.wait_dome_to_load()

    def verify_category_present(self, category_name: str) -> None:
        """
        Verify if a category is present in the search results.

        :param category_name: str, the name of the category to verify.
        :return: bool, True if the category is present, False otherwise.
        """
        xpath = self._format_tuple(Locators.CATEGORY_LINK, category_name)
        elements = self.find_elements_by_xpath(xpath)
        assert len(elements) > 0, (
            f"Category with name '{category_name}' not found in search results"
        )

    def open_random_available_stream(self) -> None:
        """
        Open a random stream from the list of available streams.

        :return: None
        """
        streams = self._get_all_available_streams()
        if not streams:
            raise NoSuchElementException("No streams available to open")
        random.choice(streams).click()
        self.wait_dome_to_load()

    ####################
    # Internal methods #
    ####################

    def _get_all_available_streams(self) -> list:
        """
        Get a list of all available streams on the page.

        :return: list of WebElement, all available streams.
        """
        streams = self.find_elements_by_xpath(Locators.STREAM_LIST)
        return streams
