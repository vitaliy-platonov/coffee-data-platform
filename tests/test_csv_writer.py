

from src.incremental_load.writers.csv_writer import save_payments_to_csv
from src.incremental_load.writers.csv_writer import save_deliveries_to_csv
from src.incremental_load.writers.csv_writer import save_order_items_to_csv
import csv

from src.incremental_load.writers.csv_writer import (
    save_customers_to_csv,
    save_orders_to_csv,
    save_order_items_to_csv,
    save_payments_to_csv,
    save_deliveries_to_csv,
)


def test_save_customers_to_csv(tmp_path, monkeypatch):
    customers = [
        {
            "customer_id": 10001,
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone": "+79990000001",
            "email": "ivan@example.com",
            "city": "Krasnodar",
            "registration_date": "2026-08-21",
        }
    ]

    monkeypatch.setattr(
        "src.incremental_load.writers.csv_writer.INCREMENTAL_DATA_DIR",
        tmp_path,
    )

    save_customers_to_csv(customers)

    output_file = tmp_path / "customers_increment.csv"

    assert output_file.exists()

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["customer_id"] == "10001"
    assert rows[0]["email"] == "ivan@example.com"


def test_save_orders_to_csv(tmp_path, monkeypatch):
    orders = [
        {
            "order_id": 50001,
            "customer_id": 10001,
            "store_id": 1,
            "employee_id": 1,
            "order_date": "2026-08-21",
            "total_amount": 1250.50,
        }
    ]

    monkeypatch.setattr(
        "src.incremental_load.writers.csv_writer.INCREMENTAL_DATA_DIR",
        tmp_path,
    )

    save_orders_to_csv(orders)

    output_file = tmp_path / "orders_increment.csv"

    assert output_file.exists()

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["order_id"] == "50001"
    assert rows[0]["customer_id"] == "10001"
    assert float(rows[0]["total_amount"]) == 1250.50





def test_save_order_items_to_csv(tmp_path, monkeypatch):
    order_items = [
        {
            "order_item_id": 70001,
            "order_id": 50001,
            "product_id": 101,
            "quantity": 2,
            "price": 150.00,
        }
    ]

    monkeypatch.setattr(
        "src.incremental_load.writers.csv_writer.INCREMENTAL_DATA_DIR",
        tmp_path,
    )

    save_order_items_to_csv(order_items)

    output_file = tmp_path / "order_items_increment.csv"

    assert output_file.exists()

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["order_item_id"] == "70001"
    assert rows[0]["order_id"] == "50001"
    assert rows[0]["product_id"] == "101"
    assert rows[0]["quantity"] == "2"
    assert float(rows[0]["price"]) == 150.00



def test_save_payments_to_csv(tmp_path, monkeypatch):
    payments = [
        {
            "payment_id": 90001,
            "order_id": 50001,
            "payment_date": "2026-08-21",
            "payment_method": "card",
            "amount": 1250.50,
            "status": "paid",
        }
    ]

    monkeypatch.setattr(
        "src.incremental_load.writers.csv_writer.INCREMENTAL_DATA_DIR",
        tmp_path,
    )

    save_payments_to_csv(payments)

    output_file = tmp_path / "payments_increment.csv"

    assert output_file.exists()

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["payment_id"] == "90001"
    assert rows[0]["order_id"] == "50001"
    assert rows[0]["payment_date"] == "2026-08-21"
    assert rows[0]["payment_method"] == "card"
    assert float(rows[0]["amount"]) == 1250.50
    assert rows[0]["status"] == "paid"



def test_save_deliveries_to_csv(tmp_path, monkeypatch):
    deliveries = [
        {
            "delivery_id": 30001,
            "supplier_id": 10,
            "store_id": 1,
            "product_id": 101,
            "quantity": 50,
            "delivery_date": "2026-08-21",
        }
    ]

    monkeypatch.setattr(
        "src.incremental_load.writers.csv_writer.INCREMENTAL_DATA_DIR",
        tmp_path,
    )

    save_deliveries_to_csv(deliveries)

    output_file = tmp_path / "deliveries_increment.csv"

    assert output_file.exists()

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["delivery_id"] == "30001"
    assert rows[0]["supplier_id"] == "10"
    assert rows[0]["store_id"] == "1"
    assert rows[0]["product_id"] == "101"
    assert rows[0]["quantity"] == "50"
    assert rows[0]["delivery_date"] == "2026-08-21"