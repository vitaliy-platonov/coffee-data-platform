
import logging

import logging_config

from load_customer_mart import load_customer_mart
from load_product_mart import load_product_mart
from load_sales_mart import load_sales_mart
from load_store_mart import load_store_mart


LOGGER = logging.getLogger(__name__)


def run_marts_load() -> None:
    """
    Run MARTS loading pipeline.
    """

    LOGGER.info(
        "MARTS load started"
    )

    load_customer_mart()
    load_product_mart()
    load_sales_mart()
    load_store_mart()

    LOGGER.info(
        "MARTS load completed"
    )


if __name__ == "__main__":
    run_marts_load()