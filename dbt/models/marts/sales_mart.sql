
SELECT
    ord.order_date AS sale_date,
    st.store_id,
    st.store_name,
    COUNT(ord.order_key) AS orders_count,
    SUM(ord.total_amount) AS revenue,
    ROUND(AVG(ord.total_amount), 2) AS average_check
FROM core.fact_orders ord
JOIN core.dim_stores st
    ON ord.store_key = st.store_key
GROUP BY
    ord.order_date,
    st.store_id,
    st.store_name