
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.dates import parse_date
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_payments(file_path: Path) -> None:
    """
    Load payments data from CSV file into the staging.payments table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} payments from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.payments CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_payment_ids = set()

        for _, row in df.iterrows():

            payment_id = row["payment_id"]

            if payment_id in seen_payment_ids:
                LOGGER.warning(
                    f"Payment {payment_id}: duplicate payment_id in CSV"
                )
                skipped_rows += 1
                continue

            order_id = int(row["order_id"])

            payment_date = parse_date(
                normalize_text(row["payment_date"])
            )

            if payment_date is None:
                LOGGER.warning(
                    f"Payment {payment_id}: invalid payment_date"
                )
                skipped_rows += 1
                continue

            payment_method = normalize_text(
                row["payment_method"]
            )

            if not payment_method:
                LOGGER.warning(
                    f"Payment {payment_id}: payment_method is empty"
                )
                skipped_rows += 1
                continue

            if len(payment_method) > 20:
                LOGGER.warning(
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
                LOGGER.warning(
                    f"Payment {payment_id}: amount must be greater than 0"
                )
                skipped_rows += 1
                continue

            status = normalize_text(row["status"])

            if not status:
                LOGGER.warning(
                    f"Payment {payment_id}: status is empty"
                )
                skipped_rows += 1
                continue

            if len(status) > 20:
                LOGGER.warning(
                    f"Payment {payment_id}: status is longer than 20 characters"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
                INSERT INTO staging.payments (
                    payment_id,
                    order_id,
                    payment_date,
                    payment_method,
                    amount,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    payment_id,
                    order_id,
                    payment_date,
                    payment_method,
                    amount,
                    status,
                ),
            )

            loaded_rows += 1
            seen_payment_ids.add(payment_id)

        conn.commit()

        LOGGER.info(
            f"Payments loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load payments")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the payments staging loader.
    """
    file_path = RAW_DATA_DIR / "payments" / "payments.csv"
    load_payments(file_path)


if __name__ == "__main__":
    run()