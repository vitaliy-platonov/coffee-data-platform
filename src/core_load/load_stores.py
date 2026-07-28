
import logging

import logging_config

from database import get_connection

LOGGER = logging.getLogger(__name__)


def load_stores() -> None:
    """
    Load stores from staging into core.dim_stores.
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
                store_id,
                store_name,
                address,
                region,
                opening_date,
                is_active
            FROM staging.stores;
            """
        )

        rows = cursor.fetchall()
        LOGGER.info(
            f"Loaded {len(rows)} staging stores"
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
                        row[0],
                    ),
            )

            result = cursor.fetchone()

            if result is None:
                cursor.execute(
                    """
                    INSERT INTO core.dim_stores (
                        store_id,
                        store_name,
                        address,
                        region,
                        opening_date,
                        is_active
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                        (
                            row[0],
                            row[1],
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
                    UPDATE core.dim_stores
                    SET 
                        store_name = %s,
                        address = %s,
                        region = %s,
                        opening_date = %s,
                        is_active = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE store_id = %s;
                    """,
                        (
                            row[1],
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
            "Failed to load stores"
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
    Run the stores core loader.
    """
    load_stores()

if __name__ == "__main__":
    run()