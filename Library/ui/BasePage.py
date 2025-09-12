import time
from typing import Tuple, cast

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException


class Locators:
    """Locators for the Base page."""
    ANY_TEXT_OBJECT = (By.XPATH, "//*[contains(text(), '{}')]")


class BasePage:
    """
    Class representing the base page of a web application, providing common methods for interaction and navigation.
    """
    def __init__(self, driver) -> None:
        """
        Initialize the Base page object.

        :param driver: Web driver instance
        """
        self.driver = driver

    def menu_click(self, menu_name: str) -> None:
        """
        Click on a common menu item by its name.

        :param menu_name: Str, the name of the menu item to click.
        """
        try:
            xpath = self._format_tuple(Locators.ANY_TEXT_OBJECT, menu_name)
            WebDriverWait(self.driver, 30).until(ec.element_to_be_clickable(xpath)).click()
            self.wait_dome_to_load()
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Menu with name '{menu_name}' not found") from exc

    def get_clickable_element(self, xpath: tuple[str, str], timeout: int = 30) -> WebElement:
        """
        Get a clickable element by its name.

        :param xpath: tuple, the locator of the element to find.
        :param timeout: int, the maximum time to wait for the element to be clickable.
        :return: WebElement, the clickable element.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(xpath))
            return element
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Element with name '{xpath}' not found") from exc
        except TimeoutException as exc:
            raise TimeoutException(f"Element with name '{xpath}' not clickable after {timeout} seconds") from exc

    def get_present_element(self, xpath: tuple[str, str], timeout: int = 30) -> WebElement:
        """
        Get a clickable element by its name.

        :param xpath: tuple, the locator of the element to find.
        :param timeout: int, the maximum time to wait for the element to be clickable.
        :return: WebElement, the clickable element.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(xpath))
            return element
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Element with name '{xpath}' not found") from exc
        except TimeoutException as exc:
            raise TimeoutException(f"Element with name '{xpath}' not clickable after {timeout} seconds") from exc

    def find_elements_by_xpath(self, xpath: tuple) -> list[WebElement]:
        """
        Find an elements by its XPath.

        :param xpath: tuple, the locator of the elements to find.
        :return: List of WebElements, the found elements.
        """
        try:
            elements = self.driver.find_elements(*xpath)
            return elements
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Element with name '{xpath}' not found") from exc

    def find_element_by_xpath(self, xpath: tuple) -> WebElement:
        """
        Find an element by its XPath.

        :param xpath: tuple, the locator of the element to find.
        :return: WebElement, the found element.
        """
        try:
            elements = self.driver.find_element(*xpath)
            return elements
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Element with name '{xpath}' not found") from exc

    def wait_dome_to_load(self, timeout: int = 30) -> None:
        """
        Wait for the DOM to load completely.

        :param timeout: int, the maximum time to wait for the DOM to load.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException as exc:
            raise TimeoutException(f"DOM did not load after {timeout} seconds") from exc

    @staticmethod
    def explicit_wait(seconds: int) -> None:
        """
        Explicitly wait for a specified number of seconds.

        :param seconds: int, the number of seconds to wait.
        """
        time.sleep(seconds)

    def wait_for_stream_to_load(self, timeout: int = 30) -> None:
        """
        Wait for the stream video element to load completely.

        :param timeout: int, the maximum time to wait for the stream to load.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script(
                    "return document.querySelector('video') !== null && "
                    "document.querySelector('video').readyState === 4"
                )
            )
        except TimeoutException as exc:
            raise TimeoutException(f"Stream did not load after {timeout} seconds") from exc

    def take_screenshot(self, file_path: str) -> None:
        """
        Take a screenshot of the current page.

        :param file_path: str, the path to save the screenshot.
        """
        self.driver.save_screenshot(file_path)

    @staticmethod
    def _format_tuple(tpl: tuple, format_value: str) -> tuple[str, str]:
        """
        Format a tuple by replacing the second element with a formatted string.

        :param tpl: tuple to format
        :param format_value: value to insert into the string
        """
        lst = list(tpl)
        lst[1] = lst[1].format(format_value)
        tuple_from_list = cast(Tuple[str, str], tuple(lst))
        return tuple_from_list
