
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_employees() -> None:
    """
    Load employees from staging into core.dim_employees.
    """
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        inserted = 0
        updated = 0

        cursor.execute(
            """
            SELECT
                employee_id,
                first_name,
                last_name,
                hire_date,
                salary,
                position,
                is_active,
                store_id
            FROM staging.employees;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging employees"
        )

        for row in rows:
            cursor.execute(
                """
                SELECT
                    store_key
                FROM core.dim_stores
                WHERE store_id = %s;
                """,
                    (
                        row[7],
                    ),
            )

            store_result = cursor.fetchone()

            if store_result is None:
                LOGGER.warning(
                    f"Store {row[7]} not found in database"
                )
                continue

            store_key = store_result[0]

            cursor.execute(
                """
                SELECT
                    employee_key
                FROM core.dim_employees
                WHERE employee_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            employee_result = cursor.fetchone()

            if employee_result is None:
                cursor.execute(
                    """
                    INSERT INTO core.dim_employees (
                        employee_id,
                        first_name,
                        last_name,
                        hire_date,
                        salary,
                        position,
                        is_active,
                        store_key
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            store_key,
                        ),
                )

                inserted += 1
            else:
                cursor.execute(
                    """
                    UPDATE core.dim_employees
                    SET 
                        first_name = %s,
                        last_name = %s,
                        hire_date = %s,
                        salary = %s,
                        position = %s,
                        is_active = %s,
                        store_key = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE employee_id = %s;
                    """,
                        (
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            store_key,
                            row[0],
                        ),
                )

                updated += 1

        conn.commit()
        LOGGER.info(
            f"Inserted: {inserted}"
        )
        LOGGER.info(
            f"Updated: {updated}"
        )
    except Exception:
        LOGGER.exception(
            "Load_employees failed"
        )

        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run() -> None:
    """
    Run the employees core loader.
    """
    load_employees()

if __name__ == "__main__":
    run()


