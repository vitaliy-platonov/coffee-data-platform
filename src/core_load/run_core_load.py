
import logging

import logging_config

from load_categories import run as run_categories
from load_customers import run as run_customers
from load_deliveries import run as run_deliveries
from load_employees import run as run_employees
from load_order_items import run as run_order_items
from load_orders import run as run_orders
from load_payments import run as run_payments
from load_products import run as run_products
from load_stores import run as run_stores
from load_suppliers import run as run_suppliers

LOGGER = logging.getLogger(__name__)


def run_core_load() -> None:
    """
    Run the CORE loading pipeline.
    """
    LOGGER.info("CORE load started")

    run_categories()
    run_suppliers()
    run_stores()
    run_customers()
    run_products()
    run_employees()

    run_orders()
    run_order_items()
    run_payments()
    run_deliveries()

    LOGGER.info("CORE load finished")


if __name__ == "__main__":
    run_core_load()