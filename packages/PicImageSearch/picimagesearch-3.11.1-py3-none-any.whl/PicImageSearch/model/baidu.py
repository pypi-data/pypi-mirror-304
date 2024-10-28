from typing import Any

from .base import BaseSearchItem, BaseSearchResponse


class BaiDuItem(BaseSearchItem):
    """Represents a single BaiDu search result item.

    A class that processes and stores individual search result data from BaiDu image search.

    Attributes:
        origin (dict): The raw, unprocessed data of the search result item.
        thumbnail (str): URL of the thumbnail image.
        url (str): URL of the webpage containing the original image.
    """

    def __init__(self, data: dict[str, Any], **kwargs):
        """Initialize a BaiDu search result item.

        Args:
            data: A dictionary containing the raw search result data from BaiDu.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: dict[str, Any], **kwargs) -> None:
        """Parse the raw search result data into structured attributes.

        Args:
            data: Raw dictionary data from BaiDu search result.
            **kwargs: Additional keyword arguments (unused).

        Note:
            Some previously supported attributes have been deprecated:
            - similarity: Percentage of image similarity
            - title: Title of the source webpage
        """
        # deprecated attributes
        # self.similarity: float = round(float(data["simi"]) * 100, 2)
        # self.title: str = data["fromPageTitle"]
        self.thumbnail: str = data["thumbUrl"]
        self.url: str = data["fromUrl"]


class BaiDuResponse(BaseSearchResponse):
    """Encapsulates a complete BaiDu reverse image search response.

    A class that handles and stores the full response from a BaiDu reverse image search,
    including multiple search results.

    Attributes:
        origin (dict): The complete raw response data from BaiDu.
        raw (list[BaiDuItem]): List of processed search results as BaiDuItem instances.
        url (str): URL of the search results page on BaiDu.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs):
        """Initialize a BaiDu search response.

        Args:
            resp_data: The raw JSON response from BaiDu's API.
            resp_url: The URL of the search results page.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs) -> None:
        """Parse the raw response data into a list of search result items.

        Args:
            resp_data: Raw response dictionary from BaiDu's API.
            **kwargs: Additional keyword arguments (unused).

        Note:
            If resp_data is empty or invalid, an empty list will be returned.
        """
        self.raw: list[BaiDuItem] = (
            [BaiDuItem(i) for i in resp_data["data"]["list"]] if resp_data else []
        )
