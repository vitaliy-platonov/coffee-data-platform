
import os
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_order_items():
    file_path = os.path.join(INCREMENTAL_DATA_DIR, "order_items_increment.csv")
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
            INSERT INTO order_items (
                order_item_id,
                order_id,
                product_id,
                quantity,
                price
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
                           (
                               row["order_item_id"],
                               row["order_id"],
                               row["product_id"],
                               row["quantity"],
                               row["price"]
                           ))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_incremental_order_items()