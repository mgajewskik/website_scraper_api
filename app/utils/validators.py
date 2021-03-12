import validators
import requests


def is_valid_url_format(url: str) -> bool:

    return bool(validators.url(url))


def is_valid_url(url: str) -> bool:
    """ Checks if url is valid and online. """

    if not is_valid_url_format(url):
        return False

    return bool(requests.get(url).status_code == 200)
