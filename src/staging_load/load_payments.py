
from datetime import datetime
import logging
import os
import logging_config

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "payments",
    "payments.csv"
)

def load_payments():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df =pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} payments from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.payments CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_payment_ids = set()

        for _, row in df.iterrows():

            payment_id = row["payment_id"]
            if payment_id in seen_payment_ids:
                logging.warning(
                    f"Payment {payment_id}: duplicate payment_id in CSV"
                )
                skipped_rows += 1
                continue

            order_id = int(row["order_id"])

            payment_date = row["payment_date"]
            if pd.isna(payment_date):
                payment_date = ""
            else:
                payment_date = str(payment_date).strip()

            try:
                payment_date = datetime.strptime(
                    payment_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Payment {payment_id}: invalid payment_date"
                )
                skipped_rows += 1
                continue

            payment_method = row["payment_method"]
            if pd.isna(payment_method):
                payment_method = ""
            else:
                payment_method = str(payment_method).strip()

            if not payment_method:
                logging.warning(
                    f"Payment {payment_id}: payment_method is empty"
                )
                skipped_rows += 1
                continue

            if len(payment_method) > 20:
                logging.warning(
                    f"Payment {payment_id}: payment_method is longer than 20 characters"
                )
                skipped_rows += 1
                continue

            amount = row["amount"]
            if pd.isna(amount):
                amount = 0
            else:
                amount = float(amount)

            if amount <= 0:
                logging.warning(
                    f"Payment {payment_id}: amount must be greater than 0"
                )
                skipped_rows += 1
                continue

            status = row["status"]
            if pd.isna(status):
                status = ""
            else:
                status = str(status).strip()

            if not status:
                logging.warning(
                    f"Payment {payment_id}: status is empty"
                )
                skipped_rows += 1
                continue

            if len(status) > 20:
                logging.warning(
                    f"Payment {payment_id}: status is longer than 20 characters"
                )
                skipped_rows += 1
                continue

            cursor.execute("""
                INSERT INTO staging.payments (
                    payment_id,
                    order_id,
                    payment_date,
                    payment_method,
                    amount,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                payment_id,
                order_id,
                payment_date,
                payment_method,
                amount,
                status
            ))

            loaded_rows += 1
            seen_payment_ids.add(payment_id)

        conn.commit()

        logging.info(
            f"Payments loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        logging.exception("Failed to load payments")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_payments()
