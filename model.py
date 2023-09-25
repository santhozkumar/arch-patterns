
from datetime import date

from dataclasses import dataclass

from typing import Optional, Set


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta

        self.purchased_quantity = qty
        self._allocations: Set[OrderLine]

    def allocate(self, line: OrderLine):
        # self.available_quantity -= line.qty
        self._allocations.add(line)

    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
        # self.available_quantity += line.qty

    def can_allocate(self, line: OrderLine):
        return self.available_quantity>line.qty and self.sku==line.sku

    @property
    def allocated_quantity(self) -> int:
        return sum([line.qty for line in self._allocations])
    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity
