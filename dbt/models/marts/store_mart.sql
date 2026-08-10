SELECT
    st.store_id,
    st.store_name,
    st.region,
    COUNT(DISTINCT ord.order_key) AS orders_count,
    COUNT(DISTINCT ord.customer_key) AS customers_count,
    COALESCE(SUM(ord.total_amount), 0.00) AS total_revenue,
    COALESCE(ROUND(AVG(ord.total_amount), 2), 0.00) AS average_check
FROM core.dim_stores st
LEFT JOIN core.fact_orders ord
    ON st.store_key = ord.store_key
GROUP BY
    st.store_id,
    st.store_name,
    st.region