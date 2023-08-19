from .scraping_interface import IScraper
import time
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class PlandayDocs(IScraper):
    def __init__(self) -> None:
        self.name = 'Planday'
        self.target_url = 'https://help.planday.com/en/'

        self.base_url = 'https://help.planday.com/en/'



    def get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('header', recursive=True, class_='mb-1 font-primary text-2xl font-bold leading-10 text-body-primary-color')
        if not title:
            is_404 = soup.find('div', recursive=True, class_='mb-3 text-md font-semibold uppercase tracking-widest text-body-primary-color')
            if is_404:
                return is_404.get_text()
        return 'None' if not title else title.get_text()

    def get_updated(self, soup: BeautifulSoup) -> str:
        meta = soup.find('span', class_='text-body-secondary-color')
        if not meta:
            return ''
        updated = next((x for x in meta.get_text(separator=':').split(':') if x.startswith('Updated')), 'None')
        return updated

    def get_doc_links(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        if not section:
            return []
        links = section.find_all('a', recursive=True, href=True)
        planday_links = [x['href'] for x in links if x['href'].startswith(self.base_url)]
        planday_links_clean = [(x if '#' not in x else x.split('#')[0]) for x in planday_links]
        return list(set(planday_links_clean))

    def get_vid_links(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        if not section:
            return []
        links = section.find_all('iframe', recursive=True)
        vid_links = [x['src'] for x in links]
        return list(set(vid_links))

    def get_text(self, soup: BeautifulSoup) -> str:
        section = soup.find('section', class_='max-w-full w-240')
        if not section:
            return ''
        return section.get_text(separator=' ')