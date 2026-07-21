
import logging
import os
import logging_config
import pandas as pd

from config import RAW_DATA_DIR
from database import get_connection

file_path = os.path.join(
    RAW_DATA_DIR,
    "suppliers",
    "suppliers.csv"
)

def load_suppliers():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        df = pd.read_csv(file_path, encoding='utf-8')
        logging.info(f"Loaded {len(df)} suppliers from {file_path}")

        cursor.execute("""
        TRUNCATE TABLE staging.suppliers CASCADE;""")

        loaded_rows = 0
        skipped_rows = 0
        seen_supplier_ids = set()

        for _, row in df.iterrows():

            supplier_id = row['supplier_id']
            if supplier_id in seen_supplier_ids:
                logging.warning(
                    f"Supplier {supplier_id} duplicate supplier_id in CSV"
                )
                skipped_rows += 1
                continue

            supplier_name = row['supplier_name']
            if pd.isna(supplier_name):
                supplier_name = ""
            else:
                supplier_name = str(supplier_name).strip()

            if not supplier_name:
                logging.warning(
                    f"Supplier {supplier_id}: supplier_name is empty "
                )
                skipped_rows += 1
                continue

            is_active = row['is_active']
            if pd.isna(is_active):
                is_active = ""
            else:
                is_active = str(is_active).strip().lower()

            if not is_active:
                logging.warning(
                    f"Supplier {supplier_id}: is_active is empty"
                )
                skipped_rows += 1
                continue

            if len(supplier_name) > 100:
                logging.warning(
                    f"Supplier {supplier_id}: supplier_name is longer than 100 characters"
                )
                skipped_rows +=1
                continue

            cursor.execute("""
            INSERT INTO staging.suppliers (
                supplier_id,
                supplier_name,
                is_active)
            VALUES (%s, %s, %s)""",
                           (supplier_id,
                            supplier_name,
                            is_active))
            loaded_rows += 1
            seen_supplier_ids.add(supplier_id)

        conn.commit()
        logging.info(
            f"Suppliers loaded: {loaded_rows}, skipped: {skipped_rows}"
        )
    except Exception:
        logging.exception("Failed to load suppliers")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_suppliers()