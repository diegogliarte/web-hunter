from dataclasses import dataclass

from items.base_item import BaseItem


@dataclass
class ScrapedItem(BaseItem):
    name: str
    url: str
    price: float = None
    expiration_date: str = None
