
import logging
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_deliveries():
    conn = None
    cursor = None
    try:
        file_path = INCREMENTAL_DATA_DIR / "deliveries_increment.csv"

        conn = get_connection()
        cursor = conn.cursor()
        rows_loaded = 0

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                INSERT INTO deliveries (
                delivery_id,
                supplier_id,
                store_id,
                product_id,
                quantity,
                delivery_date
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
                                   row["delivery_id"],
                                   row["supplier_id"],
                                   row["store_id"],
                                   row["product_id"],
                                   row["quantity"],
                                   row["delivery_date"]
                               ))
                rows_loaded += 1
        conn.commit()
        logging.info(
            f"{rows_loaded} deliveries loaded successfully."
        )
        return rows_loaded
    except Exception as error:
        if conn:
            conn.rollback()
        logging.error(
            f"Error loading deliveries: {error}"
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_incremental_deliveries()