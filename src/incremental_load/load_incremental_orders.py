
import csv
import os
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_orders():
    file_path = os.path.join(INCREMENTAL_DATA_DIR, "orders_increment.csv")

    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
            INSERT INTO orders (
                order_id,
                customer_id,
                store_id,
                employee_id,
                order_date,
                total_amount
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
                           (
                               row["order_id"],
                               row["customer_id"],
                               row["store_id"],
                               row["employee_id"],
                               row["order_date"],
                               row["total_amount"]
                           ))
            conn.commit()

    cursor.close()
    conn.commit()

if __name__ == "__main__":
    load_incremental_orders()