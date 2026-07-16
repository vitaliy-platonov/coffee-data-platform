
import random
from config import INCREMENTAL_DATA_DIR
import csv
import os
from faker import Faker
from database import get_connection

fake = Faker()

def get_next_customer_id():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT MAX(customer_id)
    FROM customers""")

    last_customer_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return last_customer_id + 1

def generate_customers(count):
    customers = []

    next_customer_id = get_next_customer_id()

    for i in range(count):
        customer = {
            "customer_id": next_customer_id + i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number()[:20],
            "email": fake.email(),
            "city": fake.city(),
            "registration_date": fake.date()
        }

        customers.append(customer)

    return customers

def get_next_order_id():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT MAX(order_id) FROM orders""")

    next_order_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return next_order_id + 1


def generate_orders(count):
    orders = []

    next_order_id = get_next_order_id()

    customer_ids = get_existing_customers_ids()
    store_ids = get_existing_store_ids()
    employee_ids = get_existing_employee_ids()

    for i in range(count):
        order = {
            "order_id": next_order_id + i,
            "customer_id": random.choice(customer_ids),
            "store_id": random.choice(store_ids),
            "employee_id": random.choice(employee_ids),
            "order_date": fake.date_between(
                start_date="-30d",
                end_date="today"
            ),
            "total_amount": round(
                random.uniform(5, 200),
                2
            )
        }

        orders.append(order)

    return orders


def get_existing_customers_ids():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT customer_id FROM customers""")

    customer_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return customer_ids

def get_existing_store_ids():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT store_id FROM stores""")

    store_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return store_ids

def get_existing_employee_ids():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT employee_id FROM employees""")

    employee_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return employee_ids


def save_customers_to_csv(customers):
    file_path = os.path.join(INCREMENTAL_DATA_DIR,
                             "customers_increment.csv")

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "first_name",
                "last_name",
                "phone",
                "email",
                "city",
                "registration_date"
            ]
        )
        writer.writeheader()
        writer.writerows(customers)


def save_orders_to_csv(orders):
    file_path = os.path.join(INCREMENTAL_DATA_DIR,
                             "orders_increment.csv")
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file,
        fieldnames=[
            "order_id",
            "customer_id",
            "store_id",
            "employee_id",
            "order_date",
            "total_amount"
        ])
        writer.writeheader()
        writer.writerows(orders)



def generate_incremental_data():
    generate_customers()
    generate_orders()





if __name__ == "__main__":
    # customer = generate_customers(3)
    # save_customers_to_csv(customer)

    orders = generate_orders(5)
    save_orders_to_csv(orders)