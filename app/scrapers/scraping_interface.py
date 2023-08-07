import os.path as op
import time
import hashlib
from typing import List, Tuple
from urllib.parse import urljoin
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger
import datetime
#sudo apt install chromium-chromedriver


class IScraper(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.name:str = ''
        self.target_url:str = ''

        self.base_url = ''

        
    def run(self) -> pd.DataFrame:
        """
        get page -> extract body w/ 
            * url
            * title
            * updated
            * links(help.planday), 
            * links(iframe-video),
            * text
        """
        visit_queue = [self.target_url]
        visit_done = []
    
        columns=['url','title','updated','doc_links','vid_links','text']
        logger.info('Starting mapping {}.', self.name)

        article_df = pd.DataFrame(columns=columns)
        for doc_url in visit_queue:
            # get
            logger.info('Getting: {} from stack of {}', doc_url, len(visit_queue))
            res = requests.get(doc_url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'})
            logger.debug('Page content size: {}', len(res.content))
            soup = BeautifulSoup(res.content, 'html.parser')
            row_tuple = self.__scrape_documentation(soup)
            # onward
            visit_queue.remove(doc_url)
            visit_done.append(doc_url)
            new_urls = row_tuple[2]
            new_urls = [x for x in new_urls if x not in visit_queue + visit_done and x.startswith(self.base_url)]
            visit_queue += new_urls
            logger.info('Added {} new pages', len(new_urls))
            logger.debug('{}', new_urls)
            # stack
            row_df:pd.DataFrame = pd.DataFrame([[doc_url,*row_tuple]], columns=columns)
            article_df = pd.concat([article_df, row_df], ignore_index=True)
            # wait for (d)dos protection.
            time.sleep(2)
        return article_df

    @staticmethod
    def standardize_datetime(timestr:str, in_format:str) -> str:
        """
        Used to convert a datetime string to a consistent format.
        Docs: https://docs.python.org/2/library/datetime.html?highlight=strftime#strftime-and-strptime-behavior
        """
        return str(datetime.datetime.strptime(timestr, in_format).strftime('%Y-%m-%d %H:%M'))


    def __scrape_documentation(self, soup:BeautifulSoup) -> Tuple[str,str,str,str]:
        title = self.get_title(soup)
        logger.debug('Title: {}', title)
        updated = self.get_updated(soup)
        logger.debug('Updated: {}', updated)
        doc_links = self.get_doc_links(soup)
        logger.debug('Doc_links: {}', doc_links)
        vid_links = (self.get_vid_links(soup))
        logger.debug('Vid_links: {}', vid_links)
        text = self.get_text(soup)
        logger.debug('Text len: {}', len(text))
        return tuple((title,updated,doc_links,vid_links,text))


    @abstractmethod
    def get_title(self, soup:BeautifulSoup) -> str:
        """ return the title of the article, not the webpage, as a string. """
        raise NotImplementedError
    
    @abstractmethod
    def get_updated(self, soup:BeautifulSoup) -> str:
        """ return the time since last update of the article as a string."""
        raise NotImplementedError

    @abstractmethod
    def get_doc_links(self, soup:BeautifulSoup) -> str:
        """ return the links to other doc pages in the article as a string (list delimiter '$')"""
        raise NotImplementedError
    
    @abstractmethod
    def get_vid_links(self, soup:BeautifulSoup) -> str:
        """ return the links to videos in the article as a string (list delimiter '$')"""
        raise NotImplementedError

    @abstractmethod
    def get_text(self, soup:BeautifulSoup) -> str:
        """ return the text of the article as a single string. """
        raise NotImplementedError


