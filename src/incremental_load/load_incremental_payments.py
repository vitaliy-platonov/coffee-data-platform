
import os
import csv
from config import INCREMENTAL_DATA_DIR
from database import get_connection

def load_incremental_payments():
    file_path = os.path.join(INCREMENTAL_DATA_DIR,
                             "payments_increment.csv")
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO payments (
                payment_id,
                order_id,
                payment_date,
                payment_method,
                amount,
                status
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
                               row["payment_id"],
                               row["order_id"],
                               row["payment_date"],
                               row["payment_method"],
                               row["amount"],
                               row["status"]
                           ))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_incremental_payments()