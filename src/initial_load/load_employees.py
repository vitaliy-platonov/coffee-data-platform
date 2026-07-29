
import csv
import logging

import psycopg

import logging_config

from config import INITIAL_DATA_DIR
from database import get_connection


LOGGER = logging.getLogger(__name__)


def load_employees(file_path) -> int:
    """
    Load employees from initial CSV file into database.
    """

    connection = None
    rows_loaded = 0

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO employees (
                        employee_id,
                        first_name,
                        last_name,
                        hire_date,
                        salary,
                        position,
                        is_active,
                        store_id
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                    ),
                )

                rows_loaded += 1

        connection.commit()

        LOGGER.info(
            "Employees loaded: %s",
            rows_loaded,
        )

        return rows_loaded

    except psycopg.OperationalError:
        LOGGER.exception(
            "Database connection error"
        )

        return 0

    except FileNotFoundError:
        LOGGER.exception(
            "Initial employees file not found"
        )

        return 0

    finally:
        if connection:
            connection.close()


def run() -> None:
    """
    Run employees loader.
    """

    file_path = INITIAL_DATA_DIR / "employees.csv"

    load_employees(file_path)


if __name__ == "__main__":
    run()