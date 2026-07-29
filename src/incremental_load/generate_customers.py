
import logging

from faker import Faker

import logging_config

from database import get_connection


LOGGER = logging.getLogger(__name__)

fake = Faker()


def get_next_customer_id() -> int:
    """
    Get next customer ID from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(customer_id)
        FROM customers
        """
    )

    last_customer_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return last_customer_id + 1


def generate_customers(count: int) -> list:
    """
    Generate incremental customers data.
    """

    customers = []

    next_customer_id = get_next_customer_id()

    for i in range(count):
        customer = {
            "customer_id": next_customer_id + i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number()[:20],
            "email": fake.email(),
            "city": fake.city(),
            "registration_date": fake.date(),
        }

        customers.append(customer)

    return customers