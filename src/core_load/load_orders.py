
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_orders() -> None:
    """
    Load orders from staging into core.fact_orders.
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
                order_id,
                customer_id,
                store_id,
                employee_id,
                order_date,
                total_amount
            FROM staging.orders;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging orders"
        )

        for row in rows:
            cursor.execute(
                """
                SELECT
                    customer_key
                FROM core.dim_customers
                WHERE customer_id = %s;
                """,
                    (
                        row[1],
                    ),
            )

            customer_result = cursor.fetchone()

            if customer_result is None:
                LOGGER.warning(
                    f"Customer {row[1]} not found in database"
                )
                continue

            customer_key = customer_result[0]

            cursor.execute(
                """
                SELECT
                    store_key
                FROM core.dim_stores
                WHERE store_id = %s;
                """,
                    (
                        row[2],
                    ),
            )

            store_result = cursor.fetchone()

            if store_result is None:
                LOGGER.warning(
                    f"Store {row[2]} not found in database"
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
                        row[3],
                    ),
            )

            employee_result = cursor.fetchone()

            if employee_result is None:
                LOGGER.warning(
                    f"Employee {row[3]} not found in database"
                )
                continue

            employee_key = employee_result[0]

            cursor.execute(
                """
                SELECT
                    order_key
                FROM core.fact_orders
                WHERE order_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            order_result = cursor.fetchone()

            if order_result is None:
                cursor.execute(
                    """
                    INSERT INTO core.fact_orders (
                        order_id,
                        customer_key, 
                        store_key, 
                        employee_key, 
                        order_date, 
                        total_amount
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            customer_key,
                            store_key,
                            employee_key,
                            row[4],
                            row[5],
                        ),
                )

                inserted += 1

            else:
                cursor.execute(
                    """
                    UPDATE core.fact_orders
                    SET 
                        customer_key = %s,
                        store_key = %s,
                        employee_key = %s,
                        order_date = %s,
                        total_amount = %s
                    WHERE order_id = %s;
                    """,
                        (
                            customer_key,
                            store_key,
                            employee_key,
                            row[4],
                            row[5],
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
            f"Failed to load orders failed"
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
    Run the orders core loader.
    """
    load_orders()

if __name__ == "__main__":
    run()




