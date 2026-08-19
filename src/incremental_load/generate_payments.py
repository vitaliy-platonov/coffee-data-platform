
import logging
import random

from faker import Faker

import logging_config

from database import get_connection

from src.incremental_load.database_utils import (
    get_existing_order_ids,
    get_order_amounts,
)

LOGGER = logging.getLogger(__name__)

fake = Faker()


def get_next_payment_id() -> int:
    """
    Get next payment ID from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(payment_id)
        FROM payments
        """
    )

    next_payment_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_payment_id + 1




def generate_payments(count: int) -> list:
    """
    Generate incremental payments data.
    """

    payments = []

    next_payment_id = get_next_payment_id()

    order_ids = get_existing_order_ids()

    order_amounts = get_order_amounts()

    for i in range(count):

        order_id = random.choice(order_ids)

        payment = {
            "payment_id": next_payment_id + i,
            "order_id": order_id,
            "payment_date": fake.date_between(
                start_date="-30d",
                end_date="today",
            ),
            "payment_method": random.choice(
                [
                    "Card",
                    "Cash",
                    "online",
                ]
            ),
            "amount": order_amounts[order_id],
            "status": random.choice(
                [
                    "Paid",
                    "Refunded",
                ]
            ),
        }

        payments.append(payment)

    return payments