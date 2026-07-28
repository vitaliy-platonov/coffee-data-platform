
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_deliveries() -> None:
    """
    Load deliveries from staging into core.fact_deliveries.
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
                delivery_id,
                supplier_id,
                store_id,
                product_id,
                quantity,
                delivery_date
            FROM staging.deliveries;
        """
        )

        rows = cursor.fetchall()

        LOGGER.info(
            f"Loaded {len(rows)} staging deliveries"
        )

        for row in rows:

            cursor.execute(
                """
                SELECT
                    supplier_key
                FROM core.dim_suppliers
                WHERE supplier_id = %s;
                """,
                    (
                        row[1],
                    ),
            )

            supplier_result = cursor.fetchone()

            if supplier_result is None:
                LOGGER.warning(
                    f"Delivery {row[1]} not found in database"
                )
                continue

            supplier_key = supplier_result[0]

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
                    product_key
                FROM core.dim_products
                WHERE product_id = %s;
                """,
                    (
                        row[3],
                    ),
            )

            product_result = cursor.fetchone()

            if product_result is None:
                LOGGER.warning(
                    f"Product {row[3]} not found in database"
                )
                continue

            product_key = product_result[0]

            cursor.execute(
                """
                SELECT
                    delivery_key
                FROM core.fact_deliveries
                WHERE delivery_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            delivery_result = cursor.fetchone()

            if delivery_result is None:

                cursor.execute(
                    """
                    INSERT INTO core.fact_deliveries (
                        delivery_id,
                        supplier_key,
                        store_key,
                        product_key,
                        quantity,
                        delivery_date
                )
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                               (
                                   row[0],
                                   supplier_key,
                                   store_key,
                                   product_key,
                                   row[4],
                                   row[5],
                               ),
                )

                inserted += 1

            else:

                cursor.execute(
                    """
                    UPDATE core.fact_deliveries
                    SET 
                        supplier_key = %s,
                        store_key = %s,
                        product_key = %s,
                        quantity = %s,
                        delivery_date = %s
                    WHERE delivery_id = %s;
                    """,
                               (
                                   supplier_key,
                                   store_key,
                                   product_key,
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
            "Failed to load deliveries"
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
    Run the deliveries core loader.
    """
    load_deliveries()

if __name__ == "__main__":
    run()