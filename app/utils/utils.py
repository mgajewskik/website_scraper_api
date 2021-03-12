import re
from pathlib import Path
from typing import Iterable


def make_dirs(path: str):

    Path(path).mkdir(parents=True, exist_ok=True)


def get_filename_from_url(url: str) -> str:
    """ Return last part of the filename in url """

    return url.split("/")[-1]


def get_cleaned_filter(filter: Iterable[str]) -> str:

    joined_text = u" ".join(t.strip() for t in filter)
    return re.sub("\n", " ", joined_text)


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
