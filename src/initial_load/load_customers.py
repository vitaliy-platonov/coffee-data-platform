
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\customers.csv"

def load_customers(file_path):
    connection = None

    try:
        connection = psycopg.connect(
            host='localhost',
            port=5432,
            dbname='coffee_data_platform',
            user='postgres',
            password='1234'
        )

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