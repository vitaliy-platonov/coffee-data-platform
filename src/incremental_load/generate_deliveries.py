
import logging
import random

from faker import Faker

import logging_config

from database import get_connection

from src.incremental_load.database_utils import (
    get_existing_supplier_ids,
    get_existing_store_ids,
    get_existing_product_ids,
)

LOGGER = logging.getLogger(__name__)

fake = Faker()


def get_next_delivery_id() -> int:
    """
    Get next delivery ID from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(delivery_id)
        FROM deliveries
        """
    )

    next_delivery_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_delivery_id + 1




def generate_deliveries(count: int) -> list:
    """
    Generate incremental deliveries data.
    """

    deliveries = []

    next_delivery_id = get_next_delivery_id()

    supplier_ids = get_existing_supplier_ids()
    store_ids = get_existing_store_ids()
    product_ids = get_existing_product_ids()

    for i in range(count):

        delivery = {
            "delivery_id": next_delivery_id + i,
            "supplier_id": random.choice(supplier_ids),
            "store_id": random.choice(store_ids),
            "product_id": random.choice(product_ids),
            "quantity": random.randint(10, 100),
            "delivery_date": fake.date_between(
                start_date="-30d",
                end_date="today",
            ),
        }

        deliveries.append(delivery)

    return deliveries