
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_deliveries() -> None:
    """
    Export deliveries table to RAW layer.
    """
    try:
        export_table(
            table_name="deliveries",
            output_folder="deliveries"
        )

        LOGGER.info(
            "Deliveries export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export deliveries"
        )


def run() -> None:
    """
    Run deliveries export.
    """
    export_deliveries()


if __name__ == "__main__":
    run()