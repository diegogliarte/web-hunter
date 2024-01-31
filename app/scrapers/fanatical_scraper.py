import logging
from datetime import datetime

import requests

from items.base_item import BaseItem
from items.error_item import ErrorItem
from items.scraped_item import ScrapedItem
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class FanaticalScraper(BaseScraper):
    BASE_URL = "https://www.fanatical.com/api/all/en"

    def scrape(self) -> list[BaseItem]:
        try:
            response = requests.get(self.BASE_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error fetching Humble Bundle data: {e}")
            return [ErrorItem(scraper=type(self), code=response.status_code, message=str(e))]

        return self.parse_response(response.json())

    def parse_response(self, response_json: dict) -> list[BaseItem]:
        items = []

        for bundle in response_json["pickandmix"]:
            name = bundle["name"]
            slug = bundle["slug"]
            valid_until_str = bundle.get("valid_until")
            url = f"https://www.fanatical.com/en/pick-and-mix/{slug}"

            if valid_until_str:
                valid_until = datetime.strptime(valid_until_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                valid_until_formatted = valid_until.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                valid_until_formatted = None

            item = ScrapedItem(
                name=name,
                scraper=type(self),
                url=url,
                expiration_date=valid_until_formatted,
            )
            items.append(item)

        return items
