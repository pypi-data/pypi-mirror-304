from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..usables.item import Item


@dataclass
class TradingItem:
    item: Item
    price: int
    count: int = 1
    factor: float = 1.0
    available: int = 1
    tid: int = 0

    def __eq__(self, other):
        return self.tid == other.tid
