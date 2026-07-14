
from database import get_connection
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\products.csv"

def load_products(file_path):
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """INSERT INTO products (
                    product_id,
                    product_name,
                    price,
                    category_id,
                    supplier_id)
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
    load_products(file_path)