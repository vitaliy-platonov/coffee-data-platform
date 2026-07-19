
import logging
import csv
import os
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_customers():
    conn = None
    cursor = None
    try:
        file_path = os.path.join(
            INCREMENTAL_DATA_DIR,
            "customers_increment.csv"
        )

        conn = get_connection()
        cursor = conn.cursor()

        rows_loaded = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute("""
                INSERT INTO customers (
                    customer_id,
                    first_name,
                    last_name,
                    phone,
                    email,
                    city,
                    registration_date
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                               (
                                   row["customer_id"],
                                   row["first_name"],
                                   row["last_name"],
                                   row["phone"],
                                   row["email"],
                                   row["city"],
                                   row["registration_date"]
                               ))
                rows_loaded += 1
            conn.commit()
            logging.info(
                f"{rows_loaded} customers loaded successfully."
            )
            return rows_loaded

    except Exception as error:
        if conn:
            conn.rollback()
        logging.error(
            f"Error loading customers: {error}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == "__main__":
    load_incremental_customers()