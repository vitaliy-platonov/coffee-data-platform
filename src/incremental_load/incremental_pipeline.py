
import logging

import logging_config

from src.incremental_load.generate_customers import generate_customers
from src.incremental_load.generate_orders import generate_orders
from src.incremental_load.generate_order_items import generate_order_items
from src.incremental_load.generate_payments import generate_payments
from src.incremental_load.generate_deliveries import generate_deliveries

from src.incremental_load.writers.csv_writer import (
    save_customers_to_csv,
    save_orders_to_csv,
    save_order_items_to_csv,
    save_payments_to_csv,
    save_deliveries_to_csv,
)

from src.incremental_load.load_customers import run as run_customers
from src.incremental_load.load_orders import run as run_orders
from src.incremental_load.load_order_items import run as run_order_items
from src.incremental_load.load_payments import run as run_payments
from src.incremental_load.load_deliveries import run as run_deliveries


LOGGER = logging.getLogger(__name__)


def run() -> None:
    """
    Run incremental load pipeline.
    """

    LOGGER.info(
        "Incremental load pipeline started"
    )

    customers = generate_customers(5)
    save_customers_to_csv(customers)
    run_customers()

    orders = generate_orders(5)
    save_orders_to_csv(orders)
    run_orders()

    order_items = generate_order_items(5)
    save_order_items_to_csv(order_items)
    run_order_items()

    payments = generate_payments(5)
    save_payments_to_csv(payments)
    run_payments()

    deliveries = generate_deliveries(5)
    save_deliveries_to_csv(deliveries)
    run_deliveries()

    LOGGER.info(
        "Incremental load pipeline completed successfully"
    )


if __name__ == "__main__":
    run()