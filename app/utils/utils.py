import os
import re
from pathlib import Path
from typing import Iterable

from app.settings import DATA_PATH


def make_dirs(path: str):

    Path(path).mkdir(parents=True, exist_ok=True)


def get_filename_from_url(url: str) -> str:
    """ Return last part of the filename in url """

    return url.split("/")[-1]


def get_cleaned_filter(filter: Iterable[str]) -> str:
    """ Join whitespace stripped elements of the filter strings. """

    joined_text = " ".join(t.strip() for t in filter)
    return re.sub("\n", " ", joined_text).strip()


def remove_get_pair(url: str) -> str:
    """
    Remove HTTP GET key value pair
    'image.jpg?c=3.2.5' -> 'image.jpg'
    """

    try:
        index = url.index("?")
        return url[:index]
    except ValueError:
        return url


def is_zipped_file(id: int) -> bool:

    return os.path.isfile(os.path.join(DATA_PATH, f"{str(id)}.zip"))


def get_zipped_filename(id: int) -> str:

    return os.path.join(DATA_PATH, f"{str(id)}.zip")
