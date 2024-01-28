from dataclasses import dataclass

from app.items.base_item import BaseItem


@dataclass
class ScrapedItem(BaseItem):
    name: str
    url: str
    price: float = None
    expiration_date: str = None
