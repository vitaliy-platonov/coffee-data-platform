
CREATE SCHEMA IF NOT EXISTS marts;

CREATE TABLE marts.sales_mart
(
    sale_date DATE NOT NULL,
    store_id INTEGER NOT NULL,
    store_name VARCHAR(100) NOT NULL,

    orders_count INTEGER NOT NULL,
    revenue NUMERIC(12,2) NOT NULL,
    average_check NUMERIC(10,2) NOT NULL,

    PRIMARY KEY (sale_date, store_id)
);


CREATE TABLE marts.customer_mart
(
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    registration_date DATE NOT NULL,

    orders_count INTEGER NOT NULL,
    total_spent NUMERIC(12,2) NOT NULL,
    average_check NUMERIC(10,2) NOT NULL
);

CREATE TABLE marts.product_mart
(
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_name VARCHAR(100) NOT NULL,

    orders_count INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    total_revenue DECIMAL(12,2) NOT NULL
);



CREATE TABLE marts.store_mart
(
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,

    orders_count INTEGER NOT NULL,
    customers_count INTEGER NOT NULL,
    total_revenue NUMERIC(12,2) NOT NULL,
    average_check NUMERIC(10,2) NOT NULL
);


