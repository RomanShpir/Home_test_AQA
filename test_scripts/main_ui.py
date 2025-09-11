from Navigation import Navigation
from BrowsePage import BrowsePage


class Ui:
    """
    Ui class that encapsulates navigation and browse page functionalities.
    """
    def __init__(self, driver) -> None:
        """
        Initialize the Ui class with a web driver.

        :param driver: Web driver instance
        """
        self.driver = driver
        self.navigation = Navigation(driver)
        self.browse_page = BrowsePage(driver)
