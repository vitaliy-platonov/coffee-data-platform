
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_suppliers() -> None:
    """
    Export suppliers table to RAW layer.
    """

    try:
        export_table(
            table_name="suppliers",
            output_folder="suppliers"
        )

        LOGGER.info(
            "Suppliers export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export suppliers"
        )


def run() -> None:
    """
    Run suppliers export
    """

    export_suppliers()


if __name__ == "__main__":
    run()