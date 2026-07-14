
from database import get_connection
import psycopg
import csv
import os
from config import INITIAL_DATA_DIR

file_path = os.path.join(INITIAL_DATA_DIR, "orders.csv")

def load_orders(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """INSERT INTO orders (
                    order_id,
                    customer_id,
                    store_id,
                    employee_id,
                    order_date,
                    total_amount)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (row[0], row[1], row[2], row[3], row[4], row[5])
                )

        connection.commit()
    except psycopg.OperationalError as error:
        print(error)
    except FileNotFoundError as error:
        print(error)
    finally:
        if connection:
            connection.close()
if __name__ == "__main__":
    load_orders(file_path)