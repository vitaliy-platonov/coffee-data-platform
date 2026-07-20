
from datetime import datetime
import logging
import os

import logging_config

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "customers",
    "customers.csv"
)


def load_customers():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        logging.info(f"Loaded {len(df)} customers from {file_path}")

        cursor.execute("""
            TRUNCATE TABLE staging.customers CASCADE;
        """)

        loaded_rows = 0
        skipped_rows = 0

        for _, row in df.iterrows():

            customer_id = row["customer_id"]

            first_name = row["first_name"].strip()
            last_name = row["last_name"].strip()
            phone = row["phone"].strip()
            email = row["email"].strip().lower()
            city = row["city"].strip()

            registration_date = row["registration_date"]

            try:
                registration_date = datetime.strptime(
                    registration_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Customer {customer_id}: invalid registration_date"
                )
                skipped_rows += 1
                continue

            if not first_name:
                logging.warning(
                    f"Customer {customer_id}: first_name is empty"
                )
                skipped_rows += 1
                continue

            if not last_name:
                logging.warning(
                    f"Customer {customer_id}: last_name is empty"
                )
                skipped_rows += 1
                continue

            if not phone:
                logging.warning(
                    f"Customer {customer_id}: phone is empty"
                )
                skipped_rows += 1
                continue

            if not email:
                logging.warning(
                    f"Customer {customer_id}: email is empty"
                )
                skipped_rows += 1
                continue

            if not city:
                logging.warning(
                    f"Customer {customer_id}: city is empty"
                )
                skipped_rows += 1
                continue

            if len(phone) > 20:
                logging.warning(
                    f"Customer {customer_id}: phone is longer than 20 characters"
                )
                skipped_rows += 1
                continue

            if len(first_name) > 100:
                logging.warning(
                    f"Customer {customer_id}: first_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(last_name) > 100:
                logging.warning(
                    f"Customer {customer_id}: last_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(email) > 100:
                logging.warning(
                    f"Customer {customer_id}: email is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(city) > 100:
                logging.warning(
                    f"Customer {customer_id}: city is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO staging.customers (
                    customer_id,
                    first_name,
                    last_name,
                    phone,
                    email,
                    city,
                    registration_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                customer_id,
                first_name,
                last_name,
                phone,
                email,
                city,
                registration_date
            ))

            loaded_rows += 1

        conn.commit()

        logging.info(
            f"Customers loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception as error:
        logging.exception(("Failed to load customers"))
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    load_customers()