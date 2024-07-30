import pytest
from orm import batches
from datetime import date
import model
from sqlalchemy import text



def test_orderline_mapper_can_load_lines(session):
    insert_sql = text("""
        INSERT INTO order_lines (orderid, sku, qty)
        VALUES (:value1, :value2, :value3),
               (:value4, :value5, :value6),
               (:value7, :value8, :value9)
    """)
    params = {
        'value1': 'order1',
        'value2': 'RED-CHAIR',
        'value3': '12',
        'value4': 'order1',
        'value5': 'RED-TABLE',
        'value6': '13',
        'value7': 'order2',
        'value8': 'BLUE-LIPSTICK',
        'value9': '14',
    }
    session.execute( insert_sql, params)
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14)]

    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    line = model.OrderLine('order1', 'Decorative-Widget', 12)
    session.add(line)
    session.commit()

    rows = list(session.execute(text('Select orderid, sku, qty from order_lines')))
    assert rows == [('order1', 'Decorative-Widget', 12)]


def test_retreiving_batches(session):
    insert_sql = text( '''INSERT INTO batches (reference, sku, _purchased_quantity)
                         VALUES (:value1, :value2, :value3, :value4),
                             (:value5, :value6, :value7, :value8)
                         ''')
    params = { 
              'value1': 'batch1',
                'value2': 'RED-CHAIR',
                'value3': '100',
                'value4': None,
                'value5': 'batch1',
                'value6': 'RED-TABLE',
                'value7': '100',
                'value8': '2011-04-11'
                        }

    session.execute(insert_sql,params)
    expected = [model.Batch('batch1', 'RED-CHAIR', 100, eta=None),
                model.Batch('batch1', 'RED-CHAIR', 100, eta=date(2011,4,11))
                ]
    assert session.query(model.Batch).all() == expected
