
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


def run_core_load():
    logging.info("CORE load started")

    load_categories()
    load_suppliers()
    load_stores()
    load_customers()
    load_products()
    load_employees()

    load_orders()
    load_order_items()
    load_payments()
    load_deliveries()

    logging.info("CORE load finished")


if __name__ == "__main__":
    run_core_load()