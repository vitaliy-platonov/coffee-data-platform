
from database import get_connection
import psycopg
import csv
from config import INITIAL_DATA_DIR
import logging

file_path = INITIAL_DATA_DIR / "stores.csv"

def load_stores(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        rows_loaded = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:

                cursor.execute(
                    """INSERT INTO stores (
                        store_id,
                        store_name,
                        address,
                        region,
                        opening_date,
                        is_active)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                    (row[0], row[1], row[2], row[3], row[4], row[5])
                )
                rows_loaded += 1
        connection.commit()
        return rows_loaded
    except psycopg.OperationalError as error:
        logging.error(f"Database connection error: {error}")

    except FileNotFoundError as error:
        logging.error(f"File not found: {error}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    load_stores(file_path)