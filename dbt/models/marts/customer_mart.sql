SELECT
    cust.customer_id,
    cust.first_name,
    cust.last_name,
    cust.city,
    cust.registration_date,
    COUNT(ord.order_key) AS orders_count,
    COALESCE(SUM(ord.total_amount), 0.00) AS total_spent,
    COALESCE(ROUND(AVG(ord.total_amount), 2), 0.00) AS average_check
FROM core.dim_customers cust
LEFT JOIN core.fact_orders ord
    ON cust.customer_key = ord.customer_key
GROUP BY
    cust.customer_id,
    cust.first_name,
    cust.last_name,
    cust.city,
    cust.registration_date