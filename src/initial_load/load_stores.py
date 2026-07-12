
import psycopg
import csv

file_path = r"C:\Users\vital\OneDrive\Рабочий стол\coffee-data-platform\data\initial\stores.csv"

def load_stores(file_path):
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
        connection.commit()
    except psycopg.OperationalError as error:
        print(error)
    except FileNotFoundError as error:
        print(error)
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    load_stores(file_path)