from .scraping_interface import IScraper
from .planday_docs import PlandayDocs
from .planday_au_docs import PlandayAUDocs

active_scrapers = {
    'planday': PlandayDocs,
    'planday-au': PlandayAUDocs,
}