import os
import time
import shutil
import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Comment

from .settings import DATA_PATH
from .utils.log import debug
from .utils.validators import is_valid_url
from .utils.utils import (
    make_dirs,
    get_filename_from_url,
    get_cleaned_filter,
    remove_get_pair,
)


class Scraper:
    def __init__(self, url: str, id: int):
        self.url = url
        self.id = str(id)

        self.visible_tags = ["style", "script", "head", "title", "meta", "[document]"]
        self.download_path = os.path.join(DATA_PATH, self.id)
        self.text_filename = "text.txt"

        self.text = ""
        self.img_urls = list()

    def scrape(self) -> "Scraper":
        debug(f"Scraping started for {self.id}: {self.url}")
        start = time.time()

        soup = BeautifulSoup(self.get_url_text(), "html.parser")

        self._parse_text(soup)
        self._parse_img_urls(soup)

        make_dirs(self.download_path)
        self._save_text()
        self._download_images()

        shutil.make_archive(self.download_path, "zip", self.download_path)
        shutil.rmtree(self.download_path)

        debug(
            f"Archive created. All scraping finished succesfully in: {str(time.time() - start)} seconds."
        )
        return self

    def get_url_text(self) -> str:
        return requests.get(self.url).text

    def _is_tag_visible(self, element):

        return not element.parent.name in self.visible_tags and not isinstance(
            element, Comment
        )

    def _parse_text(self, soup: BeautifulSoup):

        self.text = get_cleaned_filter(
            filter(self._is_tag_visible, soup.findAll(text=True))
        )
        debug(f"Text from the url parsed, length: {len(self.text)}")

    def _parse_img_urls(self, soup: BeautifulSoup):

        for img in soup.find_all("img"):

            img_url = img.attrs.get("src")
            full_img_url = urljoin(self.url, remove_get_pair(img_url))

            if img_url and is_valid_url(full_img_url):
                self.img_urls.append(img_url)

        debug(f"Image urls from the main url extracted - {len(self.img_urls)} urls.")

    def _save_text(self):

        with open(os.path.join(self.download_path, self.text_filename), "w") as f:
            f.write(self.text)

        debug(f"Text saved into {self.download_path}")

    def _download_images(self):

        count = 0
        for img in self.img_urls:
            filename = os.path.join(self.download_path, get_filename_from_url(img))
            if is_valid_url(img):
                r = requests.get(img, stream=True)
                count += 1
                with open(filename, "wb") as f:
                    for chunk in r:
                        f.write(chunk)

        debug(f"Saved {count} images into {self.download_path}")
