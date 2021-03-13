import pytest

from app.utils.validators import is_valid_url, is_valid_url_format


@pytest.mark.parametrize(
    "url, expected",
    [
        ("google.com", False),
        ("google.pl", False),
        ("https://www.google.com", True),
        ("http://www.google.com", True),
    ],
)
def test_is_valid_url_format(url, expected):

    assert is_valid_url_format(url) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        ("google.com", False),
        ("google.pl", False),
        ("https://www.google.com", True),
        ("http://www.google.com", True),
        ("https://licensebuttons.net/p/zero/1.0/88x31.png", True),
        ("", False),
    ],
)
def test_is_valid_url(url, expected):

    assert is_valid_url(url) == expected
