import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_orders() -> None:
    """
    Export orders table to RAW layer.
    """
    try:
        export_table(
            table_name="orders",
            output_folder="orders"
        )

        LOGGER.info(
            "Orders export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export orders"
        )


def run() -> None:
    """
    Run orders export.
    """
    export_orders()


if __name__ == "__main__":
    run()