
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\categories.csv"

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
            print(row)

            cursor.execute(
                """
                INSERT INTO categories (category_id, category_name)
                VALUES (%s, %s);
                """,
                (row[0], row[1])
            )

    connection.commit()

except psycopg.OperationalError as e:
    print(e)

except FileNotFoundError:
    print("Файл не найден")

finally:
    if connection:
        connection.close()
