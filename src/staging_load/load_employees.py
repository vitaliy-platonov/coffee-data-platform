
from datetime import datetime
import logging
import os
import logging_config

import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "employees",
    "employees.csv"
)

def load_employees():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path,encoding='utf-8')
        logging.info(f"Loaded {len(df)} employees from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.employees CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_employee_ids = set()

        for _, row in df.iterrows():

            employee_id = row['employee_id']
            if employee_id in seen_employee_ids:
                logging.warning(
                    f"Employee {employee_id}: duplicate employee_id in CSV"
                )
                skipped_rows += 1
                continue

            first_name = row['first_name']
            if pd.isna(first_name):
                first_name = ""
            else:
                first_name = str(first_name).strip()

            if not first_name:
                logging.warning(
                    f"Employee {employee_id}: first_name is empty"
                )
                skipped_rows += 1
                continue

            if len(first_name) > 100:
                logging.warning(
                    f"Employee {employee_id}: first_name is longer than 100 characters"
                )
                skipped_rows += 1
                continue

            last_name = row['last_name']
            if pd.isna(last_name):
                last_name = ""
            else:
                last_name = str(last_name).strip()

            if not last_name:
                logging.warning(
                    f"Employee {employee_id}: last_name is empty"
                )
                skipped_rows += 1
                continue

            if len(last_name) > 50:
                logging.warning(
                    f"Employee {employee_id}: last_name longer than 50 characters"
                )
                skipped_rows += 1
                continue

            hire_date = row['hire_date']
            if pd.isna(hire_date):
                hire_date = ""
            else:
                hire_date = str(hire_date).strip()

            try:
                hire_date = datetime.strptime(
                    hire_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                logging.warning(
                    f"Employee {employee_id}: invalid hire date"
                )
                skipped_rows += 1
                continue


            salary = row['salary']
            if pd.isna(salary):
                salary = 0
            else:
                salary = float(salary)


            if salary < 0:
                logging.warning(
                    f"Employee {employee_id}: salary is negative"
                )
                skipped_rows += 1
                continue

            is_active = row['is_active']
            if pd.isna(is_active):
                is_active = ""
            else:
                is_active = str(is_active).strip()

            if not is_active:
                logging.warning(
                    f"Employee {employee_id}: is_active is empty"
                )
                skipped_rows += 1
                continue

            position = row['position']
            if pd.isna(position):
                position = ""
            else:
                position = str(position).strip()

            if not position:
                logging.warning(
                    f"Employee {employee_id}: position is empty"
                )
                skipped_rows += 1
                continue

            if len(position) > 50:
                logging.warning(
                    f"Employee {employee_id}: position is longer than 50 characters"
                )
                skipped_rows += 1
                continue

            store_id = int(row['store_id'])

            cursor.execute("""
            INSERT INTO staging.employees (
                employee_id,
                first_name,
                last_name,
                hire_date,
                salary,
                position,
                is_active,
                store_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                           (employee_id,
                            first_name,
                            last_name,
                            hire_date,
                            salary,
                            position,
                            is_active,
                            store_id
                            ))
            loaded_rows += 1
            seen_employee_ids.add(employee_id)

        conn.commit()
        logging.info(
            f"Employees loaded: {loaded_rows}, skipped: {skipped_rows} "
        )
    except Exception:
        logging.exception("Failed to load employees")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_employees()
