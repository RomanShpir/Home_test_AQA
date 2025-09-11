from Navigation import Navigation
from BrowsePage import BrowsePage


class Ui:
    """

    """
    def __init__(self, driver) -> None:
        """

        """
        self.driver = driver
        self.navigation = Navigation(driver)
        self.browse_page = BrowsePage(driver)
