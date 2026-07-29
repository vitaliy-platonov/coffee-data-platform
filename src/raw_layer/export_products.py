
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_products() -> None:
    """
    Export products table to RAW layer.
    """

    try:
        export_table(
            table_name="products",
            output_folder="products"
        )

        LOGGER.info(
            "Products export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export productsx"
        )


def run() -> None:
    """
    Run products export
    """

    export_products()


if __name__ == "__main__":
    run()