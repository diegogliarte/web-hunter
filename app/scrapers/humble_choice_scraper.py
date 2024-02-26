import datetime
import json
import logging

import requests
import bs4

from items.base_item import BaseItem
from items.error_item import ErrorItem
from items.scraped_item import ScrapedItem
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HumbleChoiceScraper(BaseScraper):
    BASE_URL = "https://www.humblebundle.com/membership"

    def scrape(self) -> list[BaseItem]:
        try:
            url = self.generate_url()
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            if response.status_code == 404:
                return []
            logger.error(f"Error fetching Humble Bundle data: {e}")
            return [ErrorItem(scraper=type(self), code=response.status_code, message=str(e))]

        if url != response.url:
            return []

        return self.parse_response(response.text)

    def generate_url(self) -> str:
        now = datetime.datetime.now()

        month_name = now.strftime("%B")
        year = now.year

        return f"{self.BASE_URL}/{month_name.lower()}-{year}"

    def parse_response(self, html: str) -> list[BaseItem]:
        soup = bs4.BeautifulSoup(html, "html.parser")
        try:
            choices = soup.find("script", id="webpack-monthly-product-data").text
            choices_json = json.loads(choices)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON data: {e}")
            return [ErrorItem(scraper=type(self), message="JSON parsing error")]

        return self.extract_items(choices_json)

    def extract_items(self, choices_json: dict) -> list[BaseItem]:
        scraped_items = []

        try:
            choices_data = choices_json.get("contentChoiceOptions", {})
            choices_data = choices_data.get("contentChoiceData", {})
            choices_data = choices_data.get("game_data", {})

            for game_data in choices_data.values():
                title = game_data["title"]
                url = self.generate_url()
                scraped_item = ScrapedItem(
                    name=title,
                    scraper=type(self),
                    url=url,
                )
                scraped_items.append(scraped_item)
        except Exception as e:
            logger.error(f"Error parsing choices data: {e}")
            return [ErrorItem(scraper=type(self), message="Choices parsing error")]

        return scraped_items
