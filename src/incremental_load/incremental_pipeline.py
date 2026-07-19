

from incremental_generator import (
    generate_customers,
    save_customers_to_csv,
    generate_orders,
    save_orders_to_csv,
    generate_order_items,
    save_order_items_to_csv,
    generate_payments,
    save_payments_to_csv,
    generate_deliveries,
    save_deliveries_to_csv
)
from load_incremental_customers import load_incremental_customers
from load_incremental_orders import load_incremental_orders
from load_incremental_order_items import load_incremental_order_items
from load_incremental_payments import load_incremental_payments
from load_incremental_deliveries import load_incremental_deliveries
import logging_config

def run_incremental_load():
    customers = generate_customers(5)
    save_customers_to_csv(customers)
    load_incremental_customers()

    orders = generate_orders(5)
    save_orders_to_csv(orders)
    load_incremental_orders()

    order_items = generate_order_items(5)
    save_order_items_to_csv(order_items)
    load_incremental_order_items()

    payments = generate_payments(5)
    save_payments_to_csv(payments)
    load_incremental_payments()

    deliveries = generate_deliveries(5)
    save_deliveries_to_csv(deliveries)
    load_incremental_deliveries()

if __name__ == '__main__':
    run_incremental_load()