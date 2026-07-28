
import logging
import logging_config

from load_categories import load_categories
from load_suppliers import load_suppliers
from load_stores import load_stores
from load_customers import load_customers
from load_products import load_products
from load_employees import load_employees
from load_orders import load_orders
from load_order_items import load_order_items
from load_payments import load_payments
from load_deliveries import load_deliveries


def run_staging_load() -> None:
    logging.info("STAGING load started")

    logging.info("Loading categories...")
    load_categories()

    logging.info("Loading suppliers...")
    load_suppliers()

    logging.info("Loading stores...")
    load_stores()

    logging.info("Loading customers...")
    load_customers()

    logging.info("Loading products...")
    load_products()

    logging.info("Loading employees...")
    load_employees()

    logging.info("Loading orders...")
    load_orders()

    logging.info("Loading order items...")
    load_order_items()

    logging.info("Loading payments...")
    load_payments()

    logging.info("Loading deliveries...")
    load_deliveries()

    logging.info("STAGING load completed successfully")


if __name__ == "__main__":
    run_staging_load()