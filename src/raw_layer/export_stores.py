
import logging

import logging_config

from export_utils import export_table

LOGGER = logging.getLogger(__name__)


def export_stores() -> None:
    """
    Export stores table to RAW layer.
    """

    try:
        export_table(
            table_name="stores",
            output_folder="stores"
        )

        LOGGER.info(
            "Store export completed"
        )

    except Exception:
        LOGGER.exception(
            "Failed to export stores"
        )


def run() -> None:
    """
    Run stores export
    """

    export_stores()


if __name__ == "__main__":
    run()