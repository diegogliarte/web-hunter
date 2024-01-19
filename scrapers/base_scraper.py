import abc
from typing import List

from items.base_item import BaseItem


class BaseScraper(abc.ABC):
    @abc.abstractmethod
    def scrape(self) -> List[BaseItem]:
        pass
