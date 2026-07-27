
import logging

import logging_config

from load_sales_mart import load_sales_mart
from load_customer_mart import load_customer_mart
from load_product_mart import load_product_mart
from load_store_mart import load_store_mart


def run_marts_load():
    logging.info("MARTS load started")

    load_sales_mart()
    load_customer_mart()
    load_product_mart()
    load_store_mart()

    logging.info("MARTS load completed")


if __name__ == "__main__":
    run_marts_load()