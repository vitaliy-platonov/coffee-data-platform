
import logging

import logging_config

from load_categories import run as run_categories
from load_suppliers import run as run_suppliers
from load_stores import run as run_stores
from load_customers import run as run_customers
from load_products import run as run_products
from load_employees import run as run_employees
from load_orders import run as run_orders
from load_order_items import run as run_order_items
from load_payments import run as run_payments
from load_deliveries import run as run_deliveries

LOGGER = logging.getLogger(__name__)


def run_staging_load() -> None:
    """
    Run all staging loaders.
    """
    LOGGER.info("STAGING load started")

    LOGGER.info("Loading categories...")
    run_categories()

    LOGGER.info("Loading suppliers...")
    run_suppliers()

    LOGGER.info("Loading stores...")
    run_stores()

    LOGGER.info("Loading customers...")
    run_customers()

    LOGGER.info("Loading products...")
    run_products()

    LOGGER.info("Loading employees...")
    run_employees()

    LOGGER.info("Loading orders...")
    run_orders()

    LOGGER.info("Loading order items...")
    run_order_items()

    LOGGER.info("Loading payments...")
    run_payments()

    LOGGER.info("Loading deliveries...")
    run_deliveries()

    LOGGER.info("STAGING load completed successfully")


if __name__ == "__main__":
    run_staging_load()