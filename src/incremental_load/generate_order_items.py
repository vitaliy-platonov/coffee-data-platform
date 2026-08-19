import logging
import random

import logging_config

from database import get_connection

from src.incremental_load.database_utils import (
    get_product_prices,
)

LOGGER = logging.getLogger(__name__)


def get_next_order_item_id() -> int:
    """
    Get next order item ID from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(order_item_id)
        FROM order_items
        """
    )

    next_order_item_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_order_item_id + 1


def generate_order_items(orders: list) -> list:
    """
    Generate incremental order items data.
    """

    order_items = []

    next_order_item_id = get_next_order_item_id()

    product_prices = get_product_prices()

    product_ids = list(product_prices.keys())

    for i in range(len(orders)):

        product_id = random.choice(product_ids)

        order_item = {
            "order_item_id": next_order_item_id + i,
            "order_id": orders[i]["order_id"],
            "product_id": product_id,
            "quantity": random.randint(1, 5),
            "price": product_prices[product_id],
        }

        order_items.append(order_item)

    return order_items