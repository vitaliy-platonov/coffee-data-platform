
from database import get_connection
import psycopg
import csv
import os
from config import INITIAL_DATA_DIR

file_path = os.path.join(INITIAL_DATA_DIR, "customers.csv")

def load_customers(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """INSERT INTO customers (
                        customer_id,
                        first_name,
                        last_name,
                        phone,
                        email,
                        city,
                        registration_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                )

        connection.commit()
    except psycopg.OperationalError as error:
        print(f"Database connection error: {error}")
    except FileNotFoundError as error:
        print(f"File not found: {error}")
    finally:
        if connection:
            connection.close()
if __name__ == "__main__":
    load_customers(file_path)