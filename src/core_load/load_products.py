
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_products() -> None:
    """
    Load products from staging into core.dim_products.
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
                product_id,
                product_name,
                price,
                category_id,
                supplier_id
            FROM staging.products;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging products"
        )

        for row in rows:

            cursor.execute(
                """
                SELECT
                    category_key
                FROM core.dim_categories
                WHERE category_id = %s;
                """,
                    (
                        row[3],
                    ),
            )

            category_result = cursor.fetchone()
            if category_result is None:
                LOGGER.warning(
                    f"Category {row[3]} not found in database"
                )
                continue

            category_key = category_result[0]

            cursor.execute(
                """
                SELECT
                    supplier_key
                FROM core.dim_suppliers
                WHERE supplier_id = %s;
                """,
                    (
                        row[4],
                    ),
            )

            supplier_result = cursor.fetchone()
            if supplier_result is None:
                LOGGER.warning(
                    f"Supplier {row[4]} not found in database"
                )
                continue

            supplier_key = supplier_result[0]

            cursor.execute(
                """
                SELECT
                    product_key
                FROM core.dim_products
                WHERE product_id = %s;
                """,
                    (
                        row[0],
                    ),
            )

            product_key = cursor.fetchone()

            if product_key is None:
                cursor.execute(
                    """
                    INSERT INTO core.dim_products (
                        product_id,
                        product_name,
                        price,
                        category_key,
                        supplier_key
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            row[1],
                            row[2],
                            category_key,
                            supplier_key,
                        ),
                )

                inserted += 1
            else:
                cursor.execute(
                    """
                    UPDATE core.dim_products
                    SET 
                        product_name = %s,
                        price = %s,
                        category_key = %s,
                        supplier_key = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE product_id = %s;
                    """,
                        (
                            row[1],
                            row[2],
                            category_key,
                            supplier_key,
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
            "Failed to load products"
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
    Run the products core loader.
    """
    load_products()


if __name__ == "__main__":
    run()