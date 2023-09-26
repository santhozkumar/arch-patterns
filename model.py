from datetime import date
from dataclasses import dataclass
from typing import Optional, Set, List

class OutOfStock(Exception):
    pass

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
        self._allocations: Set[OrderLine] = set()

    def __repr__(self) -> str:
        return f'Batch {self.reference}'

    def __eq__(self, other) -> bool:
        return (self.__class__ == other.__class__ and 
            self.reference == other.reference)

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        # self.available_quantity -= line.qty
        self._allocations.add(line)

    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
        # self.available_quantity += line.qty

    def can_allocate(self, line: OrderLine):
        return self.available_quantity>=line.qty and self.sku==line.sku

    @property
    def allocated_quantity(self) -> int:
        return sum([line.qty for line in self._allocations])
    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(frozen=True)
class Money:
    currency: str
    value: int

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"cannot add {self.currency} to {other.currency}")
        return Money(self.currency, self.value + other.value)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError(f"cannot Subtract {self.currency} to {other.currency}")
        return Money(self.currency, self.value - other.value)

    def __mul__(self, factor):
        return Money(self.currency, self.value * factor)


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Person:
    def __init__(self, name: Name):
        self.name = name

