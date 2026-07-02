# ER Diagram

orders

# ER Diagram

orders

- customer_id → customers.customer_id
- store_id → stores.store_id
- employee_id → employees.employee_id

order_items

- order_id → orders.order_id

payments

- order_id → orders.order_id


products

- category_id → categories.category_id
- supplier_id → suppliers.supplier_id

order_items

- product_id → products.product_id

deliveries

- product_id → products.product_id


deliveries

- supplier_id → suppliers.supplier_id
- store_id → stores.store_id
- product_id → products.product_id


employees

- store_id → stores.store_id

orders

- employee_id → employees.employee_id


payments

- order_id → orders.order_id


customers

- customer_id → orders.customer_id

stores

- store_id → employees.store_id
- store_id → orders.store_id
- store_id → deliveries.store_id


categories

- category_id → products.category_id

suppliers

- supplier_id → products.supplier_id
- supplier_id → deliveries.supplier_id