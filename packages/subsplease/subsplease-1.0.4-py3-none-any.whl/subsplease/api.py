from typing import Generator
from rich import print
import httpx
from .models import Episode
from .constants import EndPoints


class SubsPlease:
    """
    A client for interacting with the SubsPlease API, which provides anime episode information
    based on search queries.

    Attributes:
        timezone (str): The timezone for filtering episodes (default is "Asia/Calcutta").
        session (httpx.Client): The HTTP client used for making requests.
    """

    def __init__(self, timezone: str = "Asia/Calcutta") -> None:
        """
        Initializes the SubsPlease client with a specific timezone.

        Args:
            timezone (str): The timezone to use in the search requests (default: "Asia/Calcutta").
        """
        self.timezone = timezone
        self.session = httpx.Client(timeout=60)

    def search(self, query: str) -> Generator[Episode, None, None]:
        """
        Searches for episodes matching the given query and returns a generator of Episode objects.

        Args:
            query (str): The search term to look for.

        Yields:
            Generator[Episode, None, None]: A generator yielding Episode instances
            based on the search results.

        Raises:
            httpx.HTTPStatusError: If the request to the API fails.
        """
        response = self.session.get(
            EndPoints.SEARCH_ENDPOINT,
            params={
                "s": query,
                "tz": self.timezone,
            },
        )

        if response.status_code == 200:
            data: dict = response.json()
            if not data:
                return
            for _, episode_info in data.items():
                yield Episode.create(episode_info)
        else:
            print("Error:", response.status_code)
            print("Error JSON:", response.json())
