from dataclasses import dataclass

from items.base_item import BaseItem


@dataclass
class ErrorItem(BaseItem):
    message: str
    code: int = -1
