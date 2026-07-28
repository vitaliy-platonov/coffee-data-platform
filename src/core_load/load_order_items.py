
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_order_items() -> None:
    """
    Load order items from staging into core.fact_order_items.
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
                order_item_id,
                order_id,
                product_id,
                quantity,
                price
            FROM staging.order_items;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging order_items"
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
                    product_key
                FROM core.dim_products
                WHERE product_id = %s;
                """,
                    (
                        row[2],
                    ),
            )

            product_result = cursor.fetchone()

            if product_result is None:
                LOGGER.warning(
                    f"Product {row[2]} not found in database"
                )
                continue

            product_key = product_result[0]

            cursor.execute(
                """
                SELECT
                    order_item_key
                FROM core.fact_order_items
                WHERE order_item_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            order_item_result = cursor.fetchone()

            if order_item_result is None:
                cursor.execute(
                    """
                    INSERT INTO core.fact_order_items (
                        order_item_id,
                        order_key,
                        product_key,
                        quantity,
                        price
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            order_key,
                            product_key,
                            row[3],
                            row[4],
                        ),
                )

                inserted += 1

            else:
                cursor.execute(
                    """
                    UPDATE core.fact_order_items
                    SET 
                        order_key = %s,
                        product_key = %s,
                        quantity = %s,
                        price = %s
                    WHERE order_item_id = %s;
                    """,
                        (
                            order_key,
                            product_key,
                            row[3],
                            row[4],
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
            "Failed to load order_items failed"
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
    Run the order_items core loader.
    """
    load_order_items()


if __name__ == "__main__":
    run()






