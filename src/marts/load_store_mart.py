
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_store_mart() -> None:
    """
    Load stores from core into marts.store_mart.
    """

    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        LOGGER.info(
            "Loading Store Mart"
        )

        cursor.execute(
            """
            TRUNCATE TABLE marts.store_mart;
            """
        )

        cursor.execute(
            """
            INSERT INTO marts.store_mart (
                store_id,
                store_name,
                region,
                orders_count,
                customers_count,
                total_revenue,
                average_check
            )
            SELECT
                st.store_id,
                st.store_name,
                st.region,
                COUNT(DISTINCT ord.order_key) AS orders_count,
                COUNT(DISTINCT ord.customer_key) AS customers_count,
                COALESCE(SUM(ord.total_amount), 0.00) AS total_revenue,
                COALESCE(ROUND(AVG(ord.total_amount), 2), 0.00) AS average_check
            FROM core.dim_stores st
            LEFT JOIN core.fact_orders ord
                ON st.store_key = ord.store_key
            GROUP BY st.store_id,
                     st.store_name,
                     st.region;
            """
        )

        rows_inserted = cursor.rowcount

        conn.commit()

        LOGGER.info(
            f"Store Mart loaded successfully. Rows inserted: {rows_inserted}"
        )

    except Exception:
        LOGGER.exception(
            "Failed to load store mart"
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
    Run the stores mart loader.
    """
    load_store_mart()


if __name__ == "__main__":
    run()