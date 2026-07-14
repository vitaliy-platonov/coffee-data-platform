
from database import get_connection
import psycopg
import os

from load_categories import load_categories
from load_suppliers import load_suppliers
from load_stores import load_stores
from load_customers import load_customers
from load_products import load_products
from load_employees import load_employees
from load_orders import load_orders
from load_deliveries import load_deliveries
from load_payments import load_payments
from load_order_items import load_order_items

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

categories_path = os.path.join(
    project_root,
    "data",
    "initial",
    "categories.csv"
)

suppliers_path = os.path.join(
    project_root,
    "data",
    "initial",
    "suppliers.csv"
)

stores_path = os.path.join(
    project_root,
    "data",
    "initial",
    "stores.csv"
)

customers_path = os.path.join(
    project_root,
    "data",
    "initial",
    "customers.csv"
)

products_path = os.path.join(
    project_root,
    "data",
    "initial",
    "products.csv"
)

employees_path = os.path.join(
    project_root,
    "data",
    "initial",
    "employees.csv"
)

orders_path = os.path.join(
    project_root,
    "data",
    "initial",
    "orders.csv"
)

deliveries_path = os.path.join(
    project_root,
    "data",
    "initial",
    "deliveries.csv"
)

payments_path = os.path.join(
    project_root,
    "data",
    "initial",
    "payments.csv"
)

order_items_path = os.path.join(
    project_root,
    "data",
    "initial",
    "order_items.csv"
)

reset_sql_path = os.path.join(
    project_root,
    "sql",
    "reset_database.sql"
)


def reset_database():
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        with open(reset_sql_path, "r", encoding="utf-8") as file:
            sql_query = file.read()

        cursor.execute(sql_query)

        connection.commit()

    except psycopg.OperationalError as error:
        print(f"Database connection error: {error}")

    except FileNotFoundError as error:
        print(f"File not found: {error}")

    finally:
        if connection:
            connection.close()


def run_initial_load():
    reset_database()

    load_categories(categories_path)
    load_suppliers(suppliers_path)
    load_stores(stores_path)
    load_customers(customers_path)
    load_products(products_path)
    load_employees(employees_path)
    load_orders(orders_path)
    load_deliveries(deliveries_path)
    load_payments(payments_path)
    load_order_items(order_items_path)


if __name__ == "__main__":
    run_initial_load()