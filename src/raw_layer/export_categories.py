
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_categories() -> None:
    """
    Export categories table to RAW layer.
    """
    try:
        export_table(
            table_name="categories",
            output_folder="categories"
        )

        LOGGER.info(
            "Categories export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export categories"
        )


def run() -> None:
    """
    Run categories export.
    """
    export_categories()


if __name__ == "__main__":
    run()