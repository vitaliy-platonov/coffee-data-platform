
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_sales_mart() -> None:
    """
    Load sales from core into marts.sales_mart.
    """

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        LOGGER.info(
            "Loading Sales Mart"
        )

        cursor.execute(
            """
            TRUNCATE TABLE marts.sales_mart;
            """
        )

        cursor.execute(
            """
            INSERT INTO marts.sales_mart (
                sale_date,
                store_id,
                store_name,
                orders_count,
                revenue,
                average_check
            )
            SELECT
                ord.order_date,
                st.store_id,
                st.store_name,
                COUNT(ord.order_key),
                SUM(ord.total_amount),
                ROUND(AVG(ord.total_amount), 2)
            FROM core.fact_orders ord
            JOIN core.dim_stores st
                ON ord.store_key = st.store_key
            GROUP BY
                ord.order_date,
                st.store_id,
                st.store_name;
            """
        )

        rows_inserted = cursor.rowcount

        conn.commit()

        LOGGER.info(
            f"Sales Mart loaded successfully. Rows inserted: {rows_inserted}"
        )

    except Exception:
        if conn:
            conn.rollback()

        LOGGER.exception(
            "Failed to load sales mart"
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
    Run the sales mart loader.
    """
    load_sales_mart()


if __name__ == "__main__":
    run()