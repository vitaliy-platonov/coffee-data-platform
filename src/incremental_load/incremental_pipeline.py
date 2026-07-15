
from incremental_generator import generate_customers, save_customers_to_csv

def run_incremental_load():
    customers = generate_customers(10)
    save_customers_to_csv(customers)

if __name__ == '__main__':
    run_incremental_load()