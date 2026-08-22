

CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);


CREATE TABLE suppliers (
	supplier_id INTEGER PRIMARY KEY,
	supplier_name VARCHAR(100) NOT NULL,
	is_active BOOLEAN NOT NULL
);


CREATE TABLE stores (
	store_id INTEGER PRIMARY KEY,
	store_name VARCHAR(50) NOT NULL,
	address VARCHAR(200) NOT NULL,
	region VARCHAR(100) NOT NULL,
	opening_date DATE NOT NULL,
	is_active BOOLEAN NOT NULL
);


CREATE TABLE customers (
	customer_id INTEGER PRIMARY KEY,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	phone VARCHAR(20) UNIQUE NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	city VARCHAR(100) NOT NULL,
	registration_date DATE NOT NULL
);



CREATE TABLE products (
	product_id INTEGER PRIMARY KEY,
	product_name VARCHAR(50) NOT NULL,
	price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
	category_id INTEGER NOT NULL,
		FOREIGN KEY (category_id)
			REFERENCES categories(category_id),
	supplier_id INTEGER NOT NULL,
		FOREIGN KEY (supplier_id)
			REFERENCES suppliers(supplier_id)
);


CREATE TABLE employees (
	employee_id INTEGER PRIMARY KEY,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	hire_date DATE NOT NULL,
	salary DECIMAL(10,2) NOT NULL CHECK (salary >= 0),
	position VARCHAR(50) NOT NULL,
	is_active BOOLEAN NOT NULL,
	store_id INTEGER NOT NULL,
		FOREIGN KEY (store_id)
			REFERENCES stores(store_id)
);

CREATE TABLE orders (
	order_id INTEGER PRIMARY KEY,
	customer_id INTEGER NOT NULL,
		FOREIGN KEY (customer_id)
			REFERENCES customers(customer_id),
	store_id INTEGER NOT NULL,
		FOREIGN KEY (store_id)
			REFERENCES stores(store_id),
	employee_id INTEGER NOT NULL,
		FOREIGN KEY (employee_id)
			REFERENCES employees(employee_id),
	order_date DATE DEFAULT CURRENT_DATE NOT NULL,
	total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0)
);

CREATE TABLE order_items (
	order_item_id INTEGER PRIMARY KEY,
	order_id INTEGER NOT NULL,
		FOREIGN KEY (order_id)
			REFERENCES orders(order_id),
	product_id INTEGER NOT NULL,
		FOREIGN KEY (product_id)
			REFERENCES products(product_id),
	quantity INTEGER NOT NULL CHECK (quantity > 0),
	price DECIMAL(10,2) CHECK (price > 0)NOT NULL
);

CREATE TABLE payments (
	payment_id INTEGER PRIMARY KEY,
	order_id INTEGER NOT NULL,
		FOREIGN KEY (order_id)
			REFERENCES orders(order_id),
	payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
	payment_method VARCHAR(20) NOT NULL,
	amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
	status VARCHAR(20) NOT NULL
);


CREATE TABLE deliveries (
	delivery_id INTEGER PRIMARY KEY,
	supplier_id INTEGER NOT NULL,
		FOREIGN KEY (supplier_id)
			REFERENCES suppliers(supplier_id),
	store_id INTEGER NOT NULL,
		FOREIGN KEY (store_id)
			REFERENCES stores(store_id),
	product_id INTEGER NOT NULL,
		FOREIGN KEY (product_id)
			REFERENCES products(product_id),
	quantity INTEGER NOT NULL CHECK (quantity > 0),
	delivery_date DATE DEFAULT CURRENT_DATE NOT NULL
);