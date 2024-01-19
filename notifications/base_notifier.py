import abc
from typing import Dict, Type, List

from items.base_item import BaseItem
from scrapers.base_scraper import BaseScraper


class BaseNotifier(abc.ABC):
    @abc.abstractmethod
    def notify(self, scraped_data: Dict[Type[BaseScraper], List[BaseItem]]):
        pass
