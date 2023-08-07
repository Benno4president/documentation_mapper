from .scraping_interface import IScraper
import time
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class PlandayDocs(IScraper):
    def __init__(self) -> None:
        self.name = 'Planday'
        #self.target_url = 'https://help.planday.com/en/'
        self.target_url = 'https://help.planday.com/en/articles/30348-employee-information-visibility-and-access-settings'

        self.base_url = 'https://help.planday.com/en/'



    def get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('header', recursive=True, class_='mb-1 font-primary text-2xl font-bold leading-10 text-body-primary-color')
        return 'None' if not title else title.get_text()

    def get_updated(self, soup: BeautifulSoup) -> str:
        meta = soup.find('span', class_='text-body-secondary-color').get_text(separator=':')
        if not meta:
            return 'None'
        updated = next((x for x in meta.split(':') if x.startswith('Updated')), 'None')
        return updated

    def get_doc_links(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        links = section.find_all('a', recursive=True, href=True)
        return [x['href'] for x in links]

    def get_vid_links(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        links = section.find_all('div', recursive=True, source=True)
        print(links)
        exit()
        return [x['source'] for x in links]

    def get_text(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        return section.get_text(separator=' ')