
import logging
from pathlib import Path

import pandas as pd

import logging_config
from config import RAW_DATA_DIR
from database import get_connection
from utils.constants import MAX_NAME_LENGTH
from utils.dates import parse_date
from utils.text import normalize_text

LOGGER = logging.getLogger(__name__)


def load_employees(file_path: Path) -> None:
    """
    Load employees data from CSV file into the staging.employees table.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding="utf-8")
        LOGGER.info(f"Loaded {len(df)} employees from {file_path}")

        cursor.execute(
            """
            TRUNCATE TABLE staging.employees CASCADE;
            """
        )

        loaded_rows = 0
        skipped_rows = 0

        seen_employee_ids = set()

        for _, row in df.iterrows():

            employee_id = row["employee_id"]

            if employee_id in seen_employee_ids:
                LOGGER.warning(
                    f"Employee {employee_id}: duplicate employee_id in CSV"
                )
                skipped_rows += 1
                continue

            first_name = normalize_text(row["first_name"])

            if not first_name:
                LOGGER.warning(
                    f"Employee {employee_id}: first_name is empty"
                )
                skipped_rows += 1
                continue

            if len(first_name) > MAX_NAME_LENGTH:
                LOGGER.warning(
                    f"Employee {employee_id}: first_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            last_name = normalize_text(row["last_name"])

            if not last_name:
                LOGGER.warning(
                    f"Employee {employee_id}: last_name is empty"
                )
                skipped_rows += 1
                continue

            if len(last_name) > MAX_NAME_LENGTH:
                LOGGER.warning(
                    f"Employee {employee_id}: last_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            hire_date = parse_date(
                normalize_text(row["hire_date"])
            )

            if hire_date is None:
                LOGGER.warning(
                    f"Employee {employee_id}: invalid hire_date"
                )
                skipped_rows += 1
                continue

            salary = float(row["salary"])

            if salary < 0:
                LOGGER.warning(
                    f"Employee {employee_id}: salary is negative"
                )
                skipped_rows += 1
                continue

            is_active = row["is_active"]

            position = normalize_text(row["position"])

            if not position:
                LOGGER.warning(
                    f"Employee {employee_id}: position is empty"
                )
                skipped_rows += 1
                continue

            if len(position) > 50:
                LOGGER.warning(
                    f"Employee {employee_id}: position is longer than 50 characters"
                )
                skipped_rows += 1
                continue

            store_id = int(row["store_id"])

            cursor.execute(
                """
                INSERT INTO staging.employees (
                    employee_id,
                    first_name,
                    last_name,
                    hire_date,
                    salary,
                    position,
                    is_active,
                    store_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    employee_id,
                    first_name,
                    last_name,
                    hire_date,
                    salary,
                    position,
                    is_active,
                    store_id,
                ),
            )

            loaded_rows += 1
            seen_employee_ids.add(employee_id)

        conn.commit()

        LOGGER.info(
            f"Employees loaded: {loaded_rows}, skipped: {skipped_rows}"
        )

    except Exception:
        LOGGER.exception("Failed to load employees")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def run() -> None:
    """
    Run the employees staging loader.
    """
    file_path = RAW_DATA_DIR / "employees" / "employees.csv"
    load_employees(file_path)


if __name__ == "__main__":
    run()