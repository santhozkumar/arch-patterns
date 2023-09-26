from typing import Tuple
from model import Batch, OrderLine, Money, Person, Name, allocate
from model import OutOfStock
from datetime import date, datetime, timedelta
import pytest


def make_batch_and_line(sku, batch_qty, line_qty) -> Tuple[Batch, OrderLine]:
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )



def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line('Blue bottles', 20, 10)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, unalocated_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.deallocate(unalocated_line)
    assert batch.available_quantity == 20



today = datetime.now() 
tomorrow = datetime.now() + timedelta(days=1)
later  = datetime.now() + timedelta(days=4)

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)


    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    laterly = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, laterly, earliest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert laterly.available_quantity == 100

def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)

    allocated_batch_ref = allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.reference == allocated_batch_ref


def test_out_of_stock_exception():
    batch = Batch("batch-001", "RETRO-PIECE", 10, eta=tomorrow)
    line = OrderLine("oref", "RETRO-PIECE", 10)

    allocate(line, [batch])
    with pytest.raises(OutOfStock, match="RETRO-PIECE"):
        allocate(OrderLine("oref", "RETRO-PIECE", 1), [batch])

fiver = Money('gbp', 5)
tenner = Money('gbp', 10)

def test_can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def test_can_subtract_money_values():
    assert tenner - fiver == fiver

def test_adding_different_currencies_fails():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)

def test_can_multiply_money_by_a_number():
    assert fiver * 5 == Money('gbp', 25)

def test_multiplying_two_money_values_is_an_error():
    with pytest.raises(TypeError):
        tenner * fiver


def test_barry_is_harry():
    harry = Person(Name('harry', 'parcival'))
    barry = harry
    barry.name = Name('barry', 'parcival')
    print(harry.__hash__(), barry.__hash__())
    assert harry is barry and barry is harry



