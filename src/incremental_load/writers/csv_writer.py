
import csv
import logging

import logging_config

from config import INCREMENTAL_DATA_DIR


LOGGER = logging.getLogger(__name__)


def save_customers_to_csv(customers: list) -> None:
    """
    Save customers data to CSV file.
    """

    file_path = INCREMENTAL_DATA_DIR / "customers_increment.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "first_name",
                "last_name",
                "phone",
                "email",
                "city",
                "registration_date",
            ],
        )

        writer.writeheader()
        writer.writerows(customers)


def save_orders_to_csv(orders: list) -> None:
    """
    Save orders data to CSV file.
    """

    file_path = INCREMENTAL_DATA_DIR / "orders_increment.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id",
                "customer_id",
                "store_id",
                "employee_id",
                "order_date",
                "total_amount",
            ],
        )

        writer.writeheader()
        writer.writerows(orders)


def save_order_items_to_csv(order_items: list) -> None:
    """
    Save order items data to CSV file.
    """

    file_path = INCREMENTAL_DATA_DIR / "order_items_increment.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_item_id",
                "order_id",
                "product_id",
                "quantity",
                "price",
            ],
        )

        writer.writeheader()
        writer.writerows(order_items)


def save_payments_to_csv(payments: list) -> None:
    """
    Save payments data to CSV file.
    """

    file_path = INCREMENTAL_DATA_DIR / "payments_increment.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "payment_id",
                "order_id",
                "payment_date",
                "payment_method",
                "amount",
                "status",
            ],
        )

        writer.writeheader()
        writer.writerows(payments)


def save_deliveries_to_csv(deliveries: list) -> None:
    """
    Save deliveries data to CSV file.
    """

    file_path = INCREMENTAL_DATA_DIR / "deliveries_increment.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "delivery_id",
                "supplier_id",
                "store_id",
                "product_id",
                "quantity",
                "delivery_date",
            ],
        )

        writer.writeheader()
        writer.writerows(deliveries)