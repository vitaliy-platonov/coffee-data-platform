
import logging
import logging_config
from database import get_connection

def load_customer_mart():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        logging.info(f"Loading Customer Mart")

        cursor.execute("""
        TRUNCATE TABLE marts.customer_mart;
        """)

        cursor.execute("""
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
                 cust.registration_date;""")

        rows_inserted = cursor.rowcount

        conn.commit()

        logging.info(
            f"Customer Mart loaded successfully. Rows inserted: {rows_inserted}"
        )

    except Exception:
        logging.exception("Failed to Load Customer Mart")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_customer_mart()

