
from export_categories import export_categories
from export_suppliers import export_suppliers
from export_stores import export_stores
from export_customers import export_customers
from export_products import export_products
from export_employees import export_employees
from export_orders import export_orders
from export_order_items import export_order_items
from export_payments import export_payments
from export_deliveries import export_deliveries

import logging

from src import logger_config


def run_raw_export() -> None:
    logging.info("RAW export started.")

    export_categories()
    export_suppliers()
    export_stores()
    export_customers()
    export_products()
    export_employees()
    export_orders()
    export_order_items()
    export_payments()
    export_deliveries()

    logging.info("RAW export completed.")


if __name__ == "__main__":
    run_raw_export()