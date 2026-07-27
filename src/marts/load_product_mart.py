
import logging
import logging_config
from database import get_connection

def load_product_mart():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        logging.info(f"Loading Product Mart")

        cursor.execute("""
        TRUNCATE TABLE marts.product_mart;
        """)

        cursor.execute("""
        INSERT INTO marts.product_mart (
            product_id,
            product_name,
            category_name,
            orders_count,
            quantity_sold,
            total_revenue
        )

        SELECT
            pro.product_id,
            pro.product_name,
            cat.category_name,
            COUNT(ord.order_key) AS orders_count,
            COALESCE(SUM(ord.quantity), 0) AS quantity_sold,
            COALESCE(SUM(ord.quantity * ord.price), 0.00) AS total_revenue
        FROM core.dim_products pro
        JOIN core.fact_order_items ord
            ON pro.product_key = ord.product_key
        JOIN core.dim_categories cat
            ON cat.category_key = pro.category_key
        GROUP BY pro.product_id,
                 pro.product_name,
                 cat.category_name;""")

        rows_inserted = cursor.rowcount

        conn.commit()

        logging.info(
            f"Product Mart loaded successfully. Rows inserted: {rows_inserted}"
        )

    except Exception:
        logging.exception("Failed to Load Product Mart")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_product_mart()

