
import psycopg

def connection_database():
    connection = psycopg.connect(
        host='localhost',
        port=5432,
        dbname='coffee_data_platform',
        user='postgres',
        password="1234"
    )
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO categories (
                category_id,
                category_name
                )
        VALUES (
            1,
            'Coffee Beans'
            )
        ON CONFLICT (category_id) DO NOTHING;
        """
    )
    connection.commit()

    cursor.execute(
        """SELECT COUNT(*) FROM categories;"""
    )
    rows = cursor.fetchall()
    print(rows)

    cursor.close()
    connection.close()

connect = connection_database()