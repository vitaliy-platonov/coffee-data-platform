
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_customer_mart() -> None:
    """
    Load customers from core into marts.dim_customers.
    """

    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        LOGGER.info(
            "Loading Customer Mart"
        )

        cursor.execute(
            """
            TRUNCATE TABLE marts.customer_mart;
            """
        )

        cursor.execute(
            """
            INSERT INTO marts.customer_mart (
                customer_id,
                first_name,
                last_name,
                city,
                registration_date,
                orders_count,
                total_spent,
                average_check
            )
            SELECT
                cust.customer_id,
                cust.first_name,
                cust.last_name,
                cust.city,
                cust.registration_date,
                COUNT(ord.order_key) AS orders_count,
                COALESCE(SUM(ord.total_amount), 0.00) AS total_spent,
                COALESCE(ROUND(AVG(ord.total_amount), 2), 0.00) AS average_check
            FROM core.dim_customers cust
            LEFT JOIN core.fact_orders ord
                ON cust.customer_key = ord.customer_key
            GROUP BY cust.customer_id,
                     cust.first_name,
                     cust.last_name,
                     cust.city,
                     cust.registration_date;
            """
        )

        rows_inserted = cursor.rowcount

        conn.commit()

        LOGGER.info(
            f"Customer Mart loaded successfully. Rows inserted: {rows_inserted}"
        )

    except Exception:
        LOGGER.exception(
            "Failed to load customer mart"
        )

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run() -> None:
    """
    Run the customers mart loader.
    """
    load_customer_mart()

if __name__ == "__main__":
    run()

