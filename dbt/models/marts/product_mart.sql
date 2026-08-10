SELECT
    pro.product_id,
    pro.product_name,
    cat.category_name,
    COUNT(ord.order_key) AS orders_count,
    COALESCE(SUM(ord.quantity), 0) AS quantity_sold,
    COALESCE(SUM(ord.quantity * ord.price), 0.00) AS total_revenue
FROM core.dim_products pro
JOIN core.fact_order_items ord
    ON pro.product_key = ord.product_key
JOIN core.dim_categories cat
    ON cat.category_key = pro.category_key
GROUP BY
    pro.product_id,
    pro.product_name,
    cat.category_name