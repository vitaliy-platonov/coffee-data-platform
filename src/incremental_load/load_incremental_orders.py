
import logging
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_orders():
    cursor = None
    conn = None
    try:
        file_path = INCREMENTAL_DATA_DIR / "orders_increment.csv"

        conn = get_connection()
        cursor = conn.cursor()

        rows_loaded = 0

        with open(file_path, 'r',newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute("""
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    store_id,
                    employee_id,
                    order_date,
                    total_amount
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                               (
                                   row["order_id"],
                                   row["customer_id"],
                                   row["store_id"],
                                   row["employee_id"],
                                   row["order_date"],
                                   row["total_amount"]
                               ))
                rows_loaded += 1
        conn.commit()
        logging.info(
            f"{rows_loaded} orders loaded successfully."
        )
        return rows_loaded
    except Exception as error:
        if conn:
            conn.rollback()
        logging.error(
            f"Error loading orders: {error}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_incremental_orders()