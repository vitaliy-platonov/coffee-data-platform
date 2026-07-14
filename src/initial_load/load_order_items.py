
from database import get_connection
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\order_items.csv"

def load_order_items(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """INSERT INTO order_items (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    price)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (row[0], row[1], row[2], row[3], row[4])
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
    load_order_items(file_path)