from typing import List

from scrapers.base_scraper import BaseScraper
from items.scraped_item import ScrapedItem


class SteamDBScraper(BaseScraper):
    def scrape(self) -> List[ScrapedItem]:
        return []
