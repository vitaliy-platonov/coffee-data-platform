
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.dates import parse_date
from utils.text import normalize_text
from utils.constants import (
    MAX_PHONE_LENGTH,
    MAX_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_CITY_LENGTH,
)

LOGGER = logging.getLogger(__name__)


def load_customers(file_path: Path) -> None:
    """
    Load customer data from CSV file into the staging.customers table.
    """

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} customers from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.customers CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_customer_ids = set()

        for _, row in df.iterrows():

            customer_id = row["customer_id"]

            if customer_id in seen_customer_ids:
                LOGGER.warning(
                    f"Customer {customer_id}: duplicate customer_id in CSV"
                )
                skipped_rows += 1
                continue

            first_name = normalize_text(row["first_name"])

            last_name = normalize_text(row["last_name"])

            phone = normalize_text(row["phone"])

            email = normalize_text(row["email"]).lower()

            city = normalize_text(row["city"])

            registration_date = normalize_text(row["registration_date"])

            registration_date = parse_date(registration_date)

            if registration_date is None:
                LOGGER.warning(
                    f"Customer {customer_id}: invalid registration_date"
                )
                skipped_rows += 1
                continue

            if not first_name:
                LOGGER.warning(
                    f"Customer {customer_id}: first_name is empty"
                )
                skipped_rows += 1
                continue

            if not last_name:
                LOGGER.warning(
                    f"Customer {customer_id}: last_name is empty"
                )
                skipped_rows += 1
                continue

            if not phone:
                LOGGER.warning(
                    f"Customer {customer_id}: phone is empty"
                )
                skipped_rows += 1
                continue

            if not email:
                LOGGER.warning(
                    f"Customer {customer_id}: email is empty"
                )
                skipped_rows += 1
                continue

            if not city:
                LOGGER.warning(
                    f"Customer {customer_id}: city is empty"
                )
                skipped_rows += 1
                continue

            if len(phone) > MAX_PHONE_LENGTH:
                LOGGER.warning(
                    f"Customer {customer_id}: phone is longer than 20 characters"
                )
                skipped_rows += 1
                continue

            if len(first_name) > MAX_NAME_LENGTH:
                LOGGER.warning(
                    f"Customer {customer_id}: first_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(last_name) > MAX_NAME_LENGTH:
                LOGGER.warning(
                    f"Customer {customer_id}: last_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(email) > MAX_EMAIL_LENGTH:
                LOGGER.warning(
                    f"Customer {customer_id}: email is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            if len(city) > MAX_CITY_LENGTH:
                LOGGER.warning(
                    f"Customer {customer_id}: city is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            cursor.execute(
                """
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
                """,
                (
                    customer_id,
                    first_name,
                    last_name,
                    phone,
                    email,
                    city,
                    registration_date,
                ),
            )

            loaded_rows += 1
            seen_customer_ids.add(customer_id)

        conn.commit()

        LOGGER.info(
            f"Customers loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load customers")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the customers staging loader.
    """
    file_path = RAW_DATA_DIR / "customers" / "customers.csv"
    load_customers(file_path)


if __name__ == "__main__":
    run()
