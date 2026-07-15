
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

def generate_customers():
    customer_id = get_next_customer_id()

    customer = {
        "customer_id": customer_id,
        "full_name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }
    print(customer)

def generate_orders():
    pass

def generate_order_items():
    pass

def generate_payments():
    pass

def generate_deliveries():
    pass

def generate_incremental_data():
    generate_customers()
    generate_orders()
    generate_order_items()
    generate_payments()
    generate_deliveries()




if __name__ == "__main__":
    generate_customers()