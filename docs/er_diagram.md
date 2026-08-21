# Coffee Data Platform — ER-модель OLTP

## 1. Назначение

ER-модель описывает структуру операционной базы данных Coffee Data Platform и связи между основными сущностями предметной области.

## 2. Таблицы

### categories

Первичный ключ:

category_id

Поля:

- category_id;
- category_name.

### suppliers

Первичный ключ:

supplier_id

Поля:

- supplier_id;
- supplier_name;
- is_active.

### stores

Первичный ключ:

store_id

Поля:

- store_id;
- store_name;
- address;
- region;
- opening_date;
- is_active.

### customers

Первичный ключ:

customer_id

Поля:

- customer_id;
- first_name;
- last_name;
- phone;
- email;
- city;
- registration_date.

### products

Первичный ключ:

product_id

Внешние ключи:

- category_id → categories.category_id;
- supplier_id → suppliers.supplier_id.

Поля:

- product_id;
- product_name;
- price;
- category_id;
- supplier_id.

### employees

Первичный ключ:

employee_id

Внешний ключ:

store_id → stores.store_id

Поля:

- employee_id;
- first_name;
- last_name;
- hire_date;
- salary;
- position;
- is_active;
- store_id.

### orders

Первичный ключ:

order_id

Внешние ключи:

- customer_id → customers.customer_id;
- store_id → stores.store_id;
- employee_id → employees.employee_id.

Поля:

- order_id;
- customer_id;
- store_id;
- employee_id;
- order_date;
- total_amount.

### order_items

Первичный ключ:

order_item_id

Внешние ключи:

- order_id → orders.order_id;
- product_id → products.product_id.

Поля:

- order_item_id;
- order_id;
- product_id;
- quantity;
- price.

### payments

Первичный ключ:

payment_id

Внешний ключ:

order_id → orders.order_id

Поля:

- payment_id;
- order_id;
- payment_date;
- payment_method;
- amount;
- status.

### deliveries

Первичный ключ:

delivery_id

Внешние ключи:

- supplier_id → suppliers.supplier_id;
- store_id → stores.store_id;
- product_id → products.product_id.

Поля:

- delivery_id;
- supplier_id;
- store_id;
- product_id;
- quantity;
- delivery_date.

## 3. Связи между сущностями

categories → products

Одна категория может быть связана с несколькими продуктами.

suppliers → products

Один поставщик может быть связан с несколькими продуктами.

suppliers → deliveries

Один поставщик может иметь несколько поставок.

stores → employees

Один магазин может иметь несколько сотрудников.

stores → orders

Один магазин может иметь несколько заказов.

stores → deliveries

Один магазин может иметь несколько поставок.

customers → orders

Один клиент может иметь несколько заказов.

employees → orders

Один сотрудник может обслуживать несколько заказов.

orders → order_items

Один заказ может содержать несколько позиций.

orders → payments

Заказ связан с платежами.

products → order_items

Один продукт может присутствовать во многих позициях заказов.

products → deliveries

Один продукт может присутствовать во многих поставках.

## 4. Общая структура связей

customers
↓
orders
↓
order_items
↓
products
↓
categories

orders
↓
payments

stores
↓
employees

stores
↓
deliveries
↓
suppliers

products
↓
deliveries

suppliers
↓
products