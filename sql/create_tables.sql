

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

