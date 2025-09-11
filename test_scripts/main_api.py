
from IpStackPage import IpStackPage


class Api:
    """
    Api class to interact with various API endpoints.
    """
    def __init__(self, api_base_url, api_access_key) -> None:
        """
        Initialize the Api class with the base URL and access key for the API.
        :param api_base_url: Base URL of the API.
        :param api_access_key: Access key for the API.
        """
        self.ip_stack = IpStackPage(
            base_url=api_base_url,
            access_key=api_access_key
        )
