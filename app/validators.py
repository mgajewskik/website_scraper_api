import validators
import requests


def is_valid_url_format(url: str) -> bool:

    return validators.url.url(url)


def is_url_online(url: str) -> bool:

    return bool(requests.get(url).status_code == 200)


def is_valid_url(url: str) -> bool:

    return bool(is_valid_url_format(url) and is_url_online(url))
