
from .planday_docs import PlandayDocs

class PlandayAUDocs(PlandayDocs):
    def __init__(self) -> None:
        self.name = 'PlandayAU'
        self.target_url = 'https://help.planday.com.au/en-au/'

        self.base_url = 'https://help.planday.com.au/en-au/'