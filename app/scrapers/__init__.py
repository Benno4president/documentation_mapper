from .scraping_interface import IScraper
from .planday_docs import PlandayDocs

active_scrapers = {
    'planday': PlandayDocs,
}