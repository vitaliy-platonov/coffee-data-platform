
import logging

import psycopg

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

LOGGER = logging.getLogger(__name__)


def get_connection() -> psycopg.Connection:
    """
    Create PostgreSQL database connection.

    Returns:
        psycopg.Connection: Active database connection.
    """
    try:
        return psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

    except psycopg.OperationalError as error:
        LOGGER.error("Database connection failed: %s", error)
        raise

