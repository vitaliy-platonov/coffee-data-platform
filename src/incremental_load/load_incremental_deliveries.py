

import os
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_deliveries():
    file_path = os.path.join(INCREMENTAL_DATA_DIR,
                             "deliveries_increment.csv")
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO deliveries (
            delivery_id,
            supplier_id,
            store_id,
            product_id,
            quantity,
            delivery_date
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
                               row["delivery_id"],
                               row["supplier_id"],
                               row["store_id"],
                               row["product_id"],
                               row["quantity"],
                               row["delivery_date"]
                           ))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_incremental_deliveries()