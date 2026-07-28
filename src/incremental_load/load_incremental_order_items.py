
import logging
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_order_items():
    cursor = None
    conn = None
    try:
        file_path = INCREMENTAL_DATA_DIR / "order_items_increment.csv"
        conn = get_connection()
        cursor = conn.cursor()

        rows_loaded = 0

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute("""
                INSERT INTO order_items (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                               (
                                   row["order_item_id"],
                                   row["order_id"],
                                   row["product_id"],
                                   row["quantity"],
                                   row["price"]
                               ))
                rows_loaded += 1
        conn.commit()
        logging.info(
            f"{rows_loaded} order_items loaded successfully."
        )
        return rows_loaded
    except Exception as error:
        if conn:
            conn.rollback()
        logging.error(
            f"Error loading order_items: {error}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_incremental_order_items()