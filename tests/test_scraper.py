import os
from zipfile import ZipFile

import pytest
from bs4 import BeautifulSoup

from app.scraper import Scraper


def test_create_scraper():

    scraper = Scraper(url="test/url", id=1)

    assert scraper.download_path == "tests/test_data/1"


def test_scraper_parse_text(test_file, parsed_test_file):

    scraper = Scraper(url="test/url", id=1)

    soup = BeautifulSoup(test_file, "html.parser")

    scraper._parse_text(soup)

    assert scraper.text == parsed_test_file


def test_scraper_parse_img_urls(test_file):

    scraper = Scraper(url="test/url", id=1)

    soup = BeautifulSoup(test_file, "html.parser")

    scraper._parse_img_urls(soup)

    assert scraper.img_urls == ["https://licensebuttons.net/p/zero/1.0/88x31.png"]


def test_scraper_scrape(mocker, test_data_path, test_file, cleanup):
    def get_text(*args):
        return test_file

    mocker.patch("app.scraper.Scraper.get_url_text", get_text)

    scraper = Scraper(url="test/url", id=1)

    scraper.scrape()

    path = os.path.join(test_data_path, "1.zip")

    assert os.path.isfile(path)
    assert sorted(ZipFile(path).namelist()) == ["88x31.png", "text.txt"]
