
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\suppliers.csv"

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
    print("File not founder")
finally:
    if connection:
        connection.close()