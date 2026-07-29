
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_employees() -> None:
    """
    Export employees table to RAW layer.
    """
    try:
        export_table(
            table_name="employees",
            output_folder="employees"
        )

        LOGGER.info(
            "Employees export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export employees"
        )


def run() -> None:
    """
    Run employees export.
    """
    export_employees()


if __name__ == "__main__":
    run()