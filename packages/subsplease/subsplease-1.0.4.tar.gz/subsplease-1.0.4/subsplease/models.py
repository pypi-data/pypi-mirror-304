from typing import Any
from datetime import datetime
from dataclasses import dataclass
from .enums import Quality
from .constants import EndPoints


def create_quality(text: str) -> Quality:
    """
    Converts a resolution text to a Quality enum member.

    Args:
        text (str): The resolution text to convert, e.g., "1080".

    Returns:
        Quality: A Quality enum member corresponding to the given resolution.

    Raises:
        ValueError: If the provided quality text is not a valid Quality.
    """
    try:
        return Quality(f"{text}p")
    except ValueError:
        raise ValueError(
            f"Invalid quality '{text}'. Must be one of: {[quality.value for quality in Quality]}"
        )


@dataclass
class Download:
    """
    Represents a downloadable version of an episode with a specific quality.

    Attributes:
        quality (Quality): The quality of the download, represented by the Quality enum.
        magnet (str): The magnet link for downloading.
    """

    quality: Quality
    magnet: str

    def __repr__(self) -> str:
        """
        Returns a short string representation of the Download object.

        Returns:
            str: A string displaying the quality and a truncated version of the magnet link.
        """
        return f"Download(quality={self.quality}, magnet={self.magnet[:10]}...)"

    @staticmethod
    def create(raw_data: dict[str, Any]) -> "Download":
        """
        Creates a Download instance from raw dictionary data.

        Args:
            raw_data (dict[str, Any]): A dictionary containing "res" and "magnet" keys.

        Returns:
            Download: An instance of Download with parsed data.
        """
        return Download(
            quality=create_quality(raw_data["res"]),
            magnet=raw_data["magnet"],
        )


@dataclass
class Episode:
    """
    Represents an episode or movie, with download options and additional details.

    Attributes:
        show (str): The title of the show.
        episode (str): The episode number or type of the show (e.g., Movie).
        release_date (datetime): The release date and time of the episode.
        downloads (list[Download]): A list of available downloads with different qualities.
        xdcc (str): The XDCC bot link for downloading.
        image_url (str): The URL of the episode's cover image.
        page (str): A link to the episode's page on the website.
    """

    show: str
    episode: str
    release_date: datetime
    downloads: list[Download]
    xdcc: str
    image_url: str
    page: str

    @staticmethod
    def create(raw_data: dict[str, Any]) -> "Episode":
        """
        Creates an Episode instance from raw dictionary data.

        Args:
            raw_data (dict[str, Any]): A dictionary containing information about the episode,
                                       including title, episode number/type, release date,
                                       available downloads, XDCC link, image URL, and page.

        Returns:
            Episode: An instance of Episode with parsed data.
        """
        downloads = [Download.create(download) for download in raw_data["downloads"]]
        return Episode(
            show=raw_data["show"],
            episode=raw_data["episode"],
            release_date=datetime.strptime(
                raw_data["release_date"], "%a, %d %b %Y %H:%M:%S %z"
            ),
            downloads=downloads,
            xdcc=raw_data["xdcc"],
            image_url=raw_data["image_url"],
            page=f'{EndPoints.BASE_URL}/{raw_data["page"]}',
        )
