
from database import get_connection


def get_existing_order_ids() -> list:
    """
    Get existing order IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT order_id
        FROM orders
        """
    )

    order_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return order_ids


def get_existing_customers_ids() -> list:
    """
    Get existing customer IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT customer_id
        FROM customers
        """
    )

    customer_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return customer_ids


def get_existing_product_ids() -> list:
    """
    Get existing product IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id
        FROM products
        """
    )

    product_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return product_ids


def get_existing_store_ids() -> list:
    """
    Get existing store IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT store_id
        FROM stores
        """
    )

    store_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return store_ids


def get_existing_employee_ids() -> list:
    """
    Get existing employee IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT employee_id
        FROM employees
        """
    )

    employee_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return employee_ids


def get_existing_supplier_ids() -> list:
    """
    Get existing supplier IDs from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT supplier_id
        FROM suppliers
        """
    )

    supplier_ids = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return supplier_ids


def get_product_prices() -> dict:
    """
    Get product prices from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id, price
        FROM products
        """
    )

    product_prices = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    return product_prices


def get_order_amounts() -> dict:
    """
    Get order amounts from database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT order_id, total_amount
        FROM orders
        """
    )

    order_amounts = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    return order_amounts