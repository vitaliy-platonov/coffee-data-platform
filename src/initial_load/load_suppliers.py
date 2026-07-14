
from database import get_connection
import psycopg
import csv
import os
from config import INITIAL_DATA_DIR

file_path = os.path.join(INITIAL_DATA_DIR, "suppliers.csv")

def load_suppliers(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, 'r',encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:

                cursor.execute(
                    """INSERT INTO suppliers (
                        supplier_id,
                        supplier_name,
                        is_active)
                        VALUES (%s, %s, %s)""",
                    (row[0], row[1], row[2])
                )

        connection.commit()
    except psycopg.OperationalError as error:
        print(error)
    except FileNotFoundError:
        print("File not found")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    load_suppliers(file_path)