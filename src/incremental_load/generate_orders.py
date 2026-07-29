
import logging
import random

from faker import Faker

import logging_config

from database import get_connection

from src.incremental_load.database_utils import get_existing_customers_ids

LOGGER = logging.getLogger(__name__)

fake = Faker()


def get_next_order_id() -> int:
    """
    Get next order ID from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(order_id)
        FROM orders
        """
    )

    next_order_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_order_id + 1


def get_existing_store_ids() -> list:
    """
    Get existing store IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT store_id
        FROM stores
        """
    )

    store_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return store_ids


def get_existing_employee_ids() -> list:
    """
    Get existing employee IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT employee_id
        FROM employees
        """
    )

    employee_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return employee_ids


def generate_orders(count: int) -> list:
    """
    Generate incremental orders data.
    """

    orders = []

    next_order_id = get_next_order_id()

    customer_ids = get_existing_customers_ids()
    store_ids = get_existing_store_ids()
    employee_ids = get_existing_employee_ids()

    for i in range(count):
        order = {
            "order_id": next_order_id + i,
            "customer_id": random.choice(customer_ids),
            "store_id": random.choice(store_ids),
            "employee_id": random.choice(employee_ids),
            "order_date": fake.date_between(
                start_date="-30d",
                end_date="today",
            ),
            "total_amount": round(
                random.uniform(5, 200),
                2,
            ),
        }

        orders.append(order)

    return orders