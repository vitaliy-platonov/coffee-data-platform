
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

def generate_orders():
    pass

def generate_order_items():
    pass

def generate_payments():
    pass

def generate_deliveries():
    pass

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

def generate_incremental_data():
    generate_customers()
    generate_orders()
    generate_order_items()
    generate_payments()
    generate_deliveries()




if __name__ == "__main__":
    customer = generate_customers(3)
    save_customers_to_csv(customer)