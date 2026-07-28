
import logging
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_payments():
    cursor = None
    conn = None
    try:
        file_path = INCREMENTAL_DATA_DIR / "payments_increment.csv"
        conn = get_connection()
        cursor = conn.cursor()

        rows_loaded = 0

        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                INSERT INTO payments (
                    payment_id,
                    order_id,
                    payment_date,
                    payment_method,
                    amount,
                    status
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
                                   row["payment_id"],
                                   row["order_id"],
                                   row["payment_date"],
                                   row["payment_method"],
                                   row["amount"],
                                   row["status"]
                               ))
                rows_loaded += 1
        conn.commit()
        logging.info(
            f"{rows_loaded} payments loaded successfully."
        )
        return rows_loaded
    except Exception as error:
        if conn:
            conn.rollback()
        logging.error(
            f"Error loading payments: {error}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_incremental_payments()