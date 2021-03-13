import pytest

from app.utils import utils


@pytest.mark.parametrize(
    "url, expected", [("xxx?/xxx", "xxx"), ("xxx", "xxx"), ("", "")]
)
def test_get_filename_from_url(url, expected):

    assert utils.get_filename_from_url(url) == expected


@pytest.mark.parametrize(
    "filter, expected",
    [
        (["test ", "1 test ", " 23 test\n"], "test 1 test 23 test"),
        ([""], ""),
        (["test"], "test"),
    ],
)
def test_get_cleaned_filter(filter, expected):

    assert utils.get_cleaned_filter(filter) == expected


@pytest.mark.parametrize("url, expected", [("xxx?/xxx", "xxx"), ("xxx", "xxx")])
def test_remove_get_pair(url, expected):

    assert utils.remove_get_pair(url) == expected


@pytest.mark.parametrize(
    "id, expected",
    [
        (1, "data/1.zip"),
        (None, "data/None.zip"),
    ],
)
def test_get_zipped_filename(id, expected):

    assert utils.get_zipped_filename(id) == expected
