
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\orders.csv"

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