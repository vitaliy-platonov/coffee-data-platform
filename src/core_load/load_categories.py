
import logging
import logging_config
from database import get_connection

def load_categories():
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        inserted = 0
        updated = 0

        cursor.execute("""
        SELECT 
            category_id,
            category_name
        FROM staging.categories;""")

        rows = cursor.fetchall()
        logging.info(
            f"Loaded {len(rows)} staging categories"
        )

        for row in rows:
            cursor.execute("""
            SELECT
                category_key
            FROM core.dim_categories
            WHERE category_id = %s;""",
                           (row[0],))

            result = cursor.fetchone()

            if result is None:
                cursor.execute("""
                INSERT INTO core.dim_categories 
                    (category_id, category_name)
                VALUES (%s, %s);""",
                               (row[0], row[1]))
                inserted += 1

            else:
                cursor.execute("""
                UPDATE core.dim_categories
                SET category_name = %s
                WHERE category_id = %s;""",
                               (row[1], row[0]))
                updated += 1

        conn.commit()
        logging.info(f"Inserted: {inserted}")
        logging.info(f"Updated: {updated}")
    except Exception:
        logging.exception("load_categories failed")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_categories()



