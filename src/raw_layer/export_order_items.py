
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_order_items() -> None:
    """
    Export order_items table to RAW layer.
    """
    try:
        export_table(
            table_name="order_items",
            output_folder="order_items"
        )

        LOGGER.info(
            "Order items export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export order_items"
        )


def run() -> None:
    """
    Run order items export.
    """
    export_order_items()


if __name__ == "__main__":
    run()