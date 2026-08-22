
CREATE SCHEMA IF NOT EXISTS core;


CREATE TABLE core.dim_categories (
	category_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	category_id INTEGER NOT NULL UNIQUE,
	category_name VARCHAR(100) NOT NULL,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.dim_suppliers (
	supplier_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	supplier_id INTEGER NOT NULL UNIQUE,
	supplier_name VARCHAR(100) NOT NULL,
	is_active BOOLEAN NOT NULL,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.dim_stores (
	store_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	store_id INTEGER NOT NULL UNIQUE,
	store_name VARCHAR(50) NOT NULL,
	address VARCHAR(200) NOT NULL,
	region VARCHAR(100) NOT NULL,
	opening_date DATE NOT NULL,
	is_active BOOLEAN NOT NULL,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.dim_customers (
	customer_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	customer_id INTEGER NOT NULL UNIQUE,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	phone VARCHAR(20) UNIQUE NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	city VARCHAR(100) NOT NULL,
	registration_date DATE NOT NULL,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.dim_products (
	product_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	product_id INTEGER UNIQUE NOT NULL,
	product_name VARCHAR(50) NOT NULL,
	category_key INTEGER NOT NULL,
	FOREIGN KEY (category_key)
		REFERENCES core.dim_categories(category_key),
	supplier_key INTEGER NOT NULL,
	FOREIGN KEY (supplier_key)
		REFERENCES core.dim_suppliers(supplier_key),

    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.dim_employees (
	employee_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	employee_id INTEGER NOT NULL UNIQUE,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	hire_date DATE NOT NULL,
	salary DECIMAL(10,2) NOT NULL CHECK (salary >= 0),
	position VARCHAR(50) NOT NULL,
	is_active BOOLEAN NOT NULL,
	store_key INTEGER NOT NULL,
	FOREIGN KEY (store_key)
		REFERENCES core.dim_stores(store_key),

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.fact_orders (
	order_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_id INTEGER NOT NULL UNIQUE,
	customer_key INTEGER NOT NULL,
	FOREIGN KEY (customer_key)
		REFERENCES core.dim_customers(customer_key),
	store_key INTEGER NOT NULL,
	FOREIGN KEY (store_key)
		REFERENCES core.dim_stores(store_key),
	employee_key INTEGER NOT NULL,
	FOREIGN KEY (employee_key)
		REFERENCES core.dim_employees(employee_key),
	order_date DATE DEFAULT CURRENT_DATE NOT NULL,
	total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.fact_order_items (
	order_item_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	order_item_id INTEGER NOT NULL UNIQUE,
	order_key INTEGER NOT NULL,
	FOREIGN KEY (order_key)
		REFERENCES core.fact_orders(order_key),
	product_key INTEGER NOT NULL,
	FOREIGN KEY (product_key)
		REFERENCES core.dim_products(product_key),
	quantity INTEGER NOT NULL CHECK (quantity > 0),
	price DECIMAL(10,2) NOT NULL CHECK (price > 0),

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.fact_payments (
	payment_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	payment_id INTEGER NOT NULL UNIQUE,
	order_key INTEGER NOT NULL,
	FOREIGN KEY (order_key)
		REFERENCES core.fact_orders(order_key),
	payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
	payment_method VARCHAR(20) NOT NULL,
	amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
	status VARCHAR(20) NOT NULL,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE core.fact_deliveries (
	delivery_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	delivery_id INTEGER NOT NULL UNIQUE,
	supplier_key INTEGER NOT NULL,
	FOREIGN KEY (supplier_key)
		REFERENCES core.dim_suppliers(supplier_key),
	store_key INTEGER NOT NULL,
	FOREIGN KEY (store_key)
		REFERENCES core.dim_stores(store_key),
	product_key INTEGER NOT NULL,
	FOREIGN KEY (product_key)
		REFERENCES core.dim_products(product_key),
	quantity INTEGER NOT NULL CHECK (quantity > 0),
	delivery_date DATE NOT NULL DEFAULT CURRENT_DATE,

	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);