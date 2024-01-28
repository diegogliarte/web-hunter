import abc

from items.base_item import BaseItem


class BaseScraper(abc.ABC):
    @abc.abstractmethod
    def scrape(self) -> list[BaseItem]:
        pass
