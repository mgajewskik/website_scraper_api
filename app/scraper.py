import os
import shutil
import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from bs4.element import Comment

from app.utils.validators import is_valid_url
from app.utils.utils import make_dirs, get_filename_from_url, get_cleaned_filter, remove_get_pair


class Scraper:
    def __init__(self, url: str, id: int):
        self.url = url
        self.id = id

        self.visible_tags = ['style', 'script', 'head', 'title', 'meta', '[document]']
        self.download_path = os.path.join("data", str(id))
        self.text_filename = "text.txt"

        self.text = ""
        self.img_urls = list()

    def is_tag_visible(self, element):
        if element.parent.name in self.visible_tags:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def parse_text(self, soup: BeautifulSoup):

        self.text = get_cleaned_filter(filter(self.is_tag_visible, soup.findAll(text=True)))

    def parse_img_urls(self, soup: BeautifulSoup):

        for img in soup.find_all("img"):

            img_url = img.attrs.get("src")
            if not img_url:
                continue

            img_url = urljoin(self.url, remove_get_pair(img_url))
            if not is_valid_url(img_url):
                continue

            self.img_urls.append(img_url)

    def save_text(self):

        with open(os.path.join(self.download_path, self.text_filename), "w") as f:
            f.write(self.text)

    def download_images(self):

        for img in self.img_urls:
            filename = os.path.join(self.download_path, get_filename_from_url(img))
            r = requests.get(img, stream=True)
            if is_valid_url(img):
                with open(filename, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

    def scrape(self) -> "Scraper":

        soup = BeautifulSoup(requests.get(self.url).text, "html.parser")

        self.parse_text(soup)
        self.parse_img_urls(soup)

        make_dirs(self.download_path)
        self.save_text()
        self.download_images()

        shutil.make_archive(self.download_path, "zip", self.download_path)
        shutil.rmtree(self.download_path)

        return self
