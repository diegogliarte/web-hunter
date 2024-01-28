import json
import logging

import requests
import bs4

from app.items.base_item import BaseItem
from app.items.error_item import ErrorItem
from app.items.scraped_item import ScrapedItem
from app.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HumbleBundleScraper(BaseScraper):
    BASE_URL = "https://www.humblebundle.com"
    BUNDLES_URL = f"{BASE_URL}/bundles"
    CATEGORY_NAMES = ["books", "games", "software"]

    def scrape(self) -> list[BaseItem]:
        try:
            response = requests.get(self.BUNDLES_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error fetching Humble Bundle data: {e}")
            return [ErrorItem(scraper=type(self), code=response.status_code, message=str(e))]

        return self.parse_response(response.text)

    def parse_response(self, html: str) -> list[BaseItem]:
        soup = bs4.BeautifulSoup(html, "html.parser")
        try:
            bundles_json_text = soup.find("script", id="landingPage-json-data").text
            bundles_json = json.loads(bundles_json_text)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON data: {e}")
            return [ErrorItem(scraper=type(self), message="JSON parsing error")]

        return self.extract_items(bundles_json)

    def extract_items(self, bundles_json: dict) -> list[BaseItem]:
        bundles_data = bundles_json.get("data", {})

        parsed_items = []
        for category_name in self.CATEGORY_NAMES:
            category_data = bundles_data.get(category_name)

            if category_data:
                parsed_category_items = self.parse_category(category_data)
                parsed_items.extend(parsed_category_items)
            else:
                logger.warning(f"Category {category_name} not found in the JSON data")

        return parsed_items

    def parse_category(self, category: dict) -> list[BaseItem]:
        try:
            mosaic = category["mosaic"][0]
            products = mosaic["products"]
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing category data: {e}")
            return [ErrorItem(scraper=type(self), message="Category parsing error")]

        items = []
        for product in products:
            try:
                url = f"{self.BASE_URL}{product['product_url']}"
                name = product["tile_name"]
                expiration_date = product["end_date|datetime"]
                item = ScrapedItem(
                    name=name,
                    scraper=type(self),
                    url=url,
                    expiration_date=expiration_date,
                )
                items.append(item)
            except KeyError as e:
                logger.error(f"Error parsing product data: {e}")
                items.append(ErrorItem(scraper=type(self), message="Product parsing error"))

        return items
