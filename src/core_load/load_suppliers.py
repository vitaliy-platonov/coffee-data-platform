
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_suppliers() -> None:
    """
    Load suppliers from staging into core.dim_suppliers.
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
                supplier_id,
                supplier_name,
                is_active
            FROM staging.suppliers;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging suppliers"
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
                        row[0],
                    ),
            )

            result = cursor.fetchone()

            if result is None:
                cursor.execute(
                    """
                    INSERT INTO core.dim_suppliers (
                        supplier_id,
                        supplier_name,
                        is_active
                    )
                    VALUES (%s, %s, %s);
                    """,
                        (
                            row[0],
                            row[1],
                            row[2],
                        ),
                )

                inserted += 1

            else:
                cursor.execute(
                    """
                    UPDATE core.dim_suppliers
                    SET 
                        supplier_name = %s, 
                        is_active = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE supplier_id = %s;
                    """,
                       (
                           row[1],
                           row[2],
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
            "Failed to load suppliers"
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
    Run the suppliers core loader.
    """
    load_suppliers()

if __name__ == "__main__":
    run()