
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_customers() -> None:
    """
    Export customers table to RAW layer.
    """
    try:
        export_table(
            table_name="customers",
            output_folder="customers"
        )

        LOGGER.info(
            "Customers export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export customers"
        )


def run() -> None:
    """
    Run customers export.
    """
    export_customers()


if __name__ == "__main__":
    run()