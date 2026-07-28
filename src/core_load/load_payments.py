
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_payments() -> None:
    """
    Load payments from staging into core.fact_payments.
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
                payment_id,
                order_id,
                payment_date,
                payment_method,
                amount,
                status
            FROM staging.payments;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging payments"
        )

        for row in rows:
            cursor.execute(
                """
                SELECT
                    order_key
                FROM core.fact_orders
                WHERE order_id = %s;
                """,
                    (
                        row[1],
                    ),
            )

            order_result = cursor.fetchone()

            if order_result is None:
                LOGGER.warning(
                    f"Order {row[1]} not found in database"
                )
                continue

            order_key = order_result[0]

            cursor.execute(
                """
                SELECT
                    payment_key
                FROM core.fact_payments
                WHERE payment_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            payment_result = cursor.fetchone()

            if payment_result is None:
                cursor.execute(
                    """
                    INSERT INTO core.fact_payments (
                        payment_id,
                        order_key,
                        payment_date,
                        payment_method,
                        amount,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            order_key,
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                        ),
                )

                inserted += 1

            else:
                cursor.execute(
                    """
                    UPDATE core.fact_payments
                    SET 
                        order_key = %s,
                        payment_date = %s,
                        payment_method = %s,
                        amount = %s,
                        status = %s
                    WHERE payment_id = %s;
                """,
                    (
                        order_key,
                        row[2],
                        row[3],
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
            "Failed to load payments")

        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run() -> None:
    """
    Run the payments core loader.
    """
    load_payments()

if __name__ == "__main__":
    run()






