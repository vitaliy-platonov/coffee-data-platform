
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

    order_count INTEGER NOT NULL,
    total_spent NUMERIC(12,2) NOT NULL,
    average_check NUMERIC(10,2) NOT NULL
);