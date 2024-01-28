from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scrapers.base_scraper import BaseScraper


@dataclass
class BaseItem:
    scraper: type["BaseScraper"]
