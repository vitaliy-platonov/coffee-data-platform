
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_payments() -> None:
    """
    Export payments table to RAW layer.
    """
    try:
        export_table(
            table_name="payments",
            output_folder="payments"
        )

        LOGGER.info(
            "Payments export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export payments"
        )


def run() -> None:
    """
    Run payments export
    """

    export_payments()

if __name__ == "__main__":
    run()