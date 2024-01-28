import abc

from items.base_item import BaseItem
from scrapers.base_scraper import BaseScraper


class BaseNotifier(abc.ABC):
    @abc.abstractmethod
    def notify(self, scraped_data: dict[type[BaseScraper], list[BaseItem]]):
        pass
