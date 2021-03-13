import os
from zipfile import ZipFile

import pytest
from bs4 import BeautifulSoup

from app.scraper import Scraper
import app.scraper


def test_create_scraper():

    scraper = Scraper(url="test/url", id=1)

    assert scraper.download_path == "data/1"


def test_scraper_parse_text(get_test_file, get_parsed_test_file):

    scraper = Scraper(url="test/url", id=1)

    soup = BeautifulSoup(get_test_file, "html.parser")

    scraper._parse_text(soup)

    assert scraper.text == get_parsed_test_file


def test_scraper_parse_img_urls(get_test_file):

    scraper = Scraper(url="test/url", id=1)

    soup = BeautifulSoup(get_test_file, "html.parser")

    scraper._parse_img_urls(soup)

    assert scraper.img_urls == ["https://licensebuttons.net/p/zero/1.0/88x31.png"]


def test_scraper_scrape(mocker, cleanup, get_test_data_path, get_test_file):
    def get_text(*args):
        return get_test_file

    mocker.patch("app.scraper.Scraper.get_url_text", get_text)
    mocker.patch.object(app.scraper, "DATA_PATH", get_test_data_path)

    scraper = Scraper(url="test/url", id=1)

    scraper.scrape()

    path = os.path.join(get_test_data_path, "1.zip")

    assert os.path.isfile(path)
    assert sorted(ZipFile(path).namelist()) == ["88x31.png", "text.txt"]
