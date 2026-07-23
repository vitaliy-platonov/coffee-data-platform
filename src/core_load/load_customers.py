

import logging
import logging_config
from database import get_connection

def load_customers():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        inserted = 0
        updated = 0

        cursor.execute("""
        SELECT
            customer_id,
            first_name,
            last_name,
            phone,
            email,
            city,
            registration_date
        FROM staging.customers;""")

        rows = cursor.fetchall()
        logging.info(
            f"Loaded {len(rows)} staging customers"
        )

        for row in rows:
            cursor.execute("""
            SELECT
                customer_key
            FROM core.dim_customers
            WHERE customer_id = %s;""",
                           (row[0],))

            result = cursor.fetchone()

            if result is None:
                cursor.execute("""
                INSERT INTO core.dim_customers
                (customer_id, first_name, last_name, phone, email, city, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                               (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                inserted += 1
            else:
                cursor.execute("""
                UPDATE core.dim_customers
                    SET first_name = %s,
                    last_name = %s,
                    phone = %s,
                    email = %s,
                    city = %s,
                    registration_date = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE customer_id = %s;
                """,
                               (row[1], row[2], row[3], row[4], row[5], row[6], row[0]))
                updated += 1

        conn.commit()
        logging.info(f"Inserted: {inserted}")
        logging.info(f"Updated: {updated}")
    except Exception:
        logging.exception("Load_customers failed")

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    load_customers()