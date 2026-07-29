
import logging

import psycopg

import logging_config

from config import INITIAL_DATA_DIR, PROJECT_ROOT
from database import get_connection

from load_categories import run as run_categories
from load_suppliers import run as run_suppliers
from load_stores import run as run_stores
from load_customers import run as run_customers
from load_products import run as run_products
from load_employees import run as run_employees
from load_orders import run as run_orders
from load_deliveries import run as run_deliveries
from load_payments import run as run_payments
from load_order_items import run as run_order_items


LOGGER = logging.getLogger(__name__)


RESET_SQL_PATH = PROJECT_ROOT / "sql" / "reset_database.sql"


def reset_database() -> None:
    """
    Reset database using SQL script.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(
            RESET_SQL_PATH,
            "r",
            encoding="utf-8",
        ) as file:
            sql_query = file.read()

        cursor.execute(sql_query)

        connection.commit()

        LOGGER.info(
            "Database reset completed"
        )

    except psycopg.OperationalError:
        LOGGER.exception(
            "Database reset failed"
        )

    except FileNotFoundError:
        LOGGER.exception(
            "Reset SQL file not found"
        )

    finally:
        if connection:
            connection.close()


def run() -> None:
    """
    Run initial load pipeline.
    """

    LOGGER.info(
        "Initial load pipeline started"
    )

    reset_database()

    LOGGER.info(
        "Loading categories"
    )
    run_categories()

    LOGGER.info(
        "Loading suppliers"
    )
    run_suppliers()

    LOGGER.info(
        "Loading stores"
    )
    run_stores()

    LOGGER.info(
        "Loading customers"
    )
    run_customers()

    LOGGER.info(
        "Loading products"
    )
    run_products()

    LOGGER.info(
        "Loading employees"
    )
    run_employees()

    LOGGER.info(
        "Loading orders"
    )
    run_orders()

    LOGGER.info(
        "Loading deliveries"
    )
    run_deliveries()

    LOGGER.info(
        "Loading payments"
    )
    run_payments()

    LOGGER.info(
        "Loading order items"
    )
    run_order_items()

    LOGGER.info(
        "Initial load pipeline completed successfully"
    )


if __name__ == "__main__":
    run()