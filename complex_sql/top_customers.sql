-- Highly Complex SQL: Customer Lifetime Value Analysis with Cohort Segmentation

WITH monthly_sales AS (
    SELECT
        c.customer_id,
        c.customer_name,
        DATE_TRUNC('month', o.order_date) AS order_month,
        SUM(o.total_amount) AS monthly_total,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_date >= DATE('2023-01-01')
    GROUP BY c.customer_id, c.customer_name, DATE_TRUNC('month', o.order_date)
),
cohorts AS (
    SELECT
        customer_id,
        customer_name,
        MIN(order_month) AS cohort_month,
        MAX(order_month) AS last_order_month,
        SUM(monthly_total) AS lifetime_value,
        AVG(monthly_total) AS avg_monthly_spend,
        COUNT(DISTINCT order_month) AS active_months
    FROM monthly_sales
    GROUP BY customer_id, customer_name
),
segmentation AS (
    SELECT
        *,
        CASE
            WHEN lifetime_value > 10000 THEN 'High Value'
            WHEN lifetime_value > 5000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS value_segment,
        CASE
            WHEN active_months >= 12 THEN 'Loyal'
            WHEN active_months >= 6 THEN 'Regular'
            ELSE 'New'
        END AS loyalty_segment
    FROM cohorts
),
ranked_customers AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY lifetime_value DESC) AS overall_rank,
        ROW_NUMBER() OVER (PARTITION BY value_segment ORDER BY lifetime_value DESC) AS segment_rank
    FROM segmentation
),
retention_curve AS (
    SELECT
        cohort_month,
        order_month,
        COUNT(DISTINCT CASE WHEN monthly_total > 0 THEN customer_id END) AS active_customers,
        LAG(COUNT(DISTINCT CASE WHEN monthly_total > 0 THEN customer_id END)) OVER (
            PARTITION BY cohort_month ORDER BY order_month
        ) AS prev_active,
        ROUND(
            COUNT(DISTINCT CASE WHEN monthly_total > 0 THEN customer_id END) * 100.0 /
            NULLIF(LAG(COUNT(DISTINCT CASE WHEN monthly_total > 0 THEN customer_id END)) OVER (
                PARTITION BY cohort_month ORDER BY order_month
            ), 0), 2
        ) AS retention_rate
    FROM monthly_sales
    GROUP BY cohort_month, order_month
)
SELECT
    rc.customer_id,
    rc.customer_name,
    rc.lifetime_value,
    rc.avg_monthly_spend,
    rc.active_months,
    rc.value_segment,
    rc.loyalty_segment,
    rc.overall_rank,
    rc.segment_rank,
    COALESCE(rc2.retention_rate, 0) AS avg_retention_rate
FROM ranked_customers rc
LEFT JOIN (
    SELECT cohort_month, AVG(retention_rate) AS retention_rate
    FROM retention_curve
    GROUP BY cohort_month
) rc2 ON rc.cohort_month = rc2.cohort_month
WHERE rc.overall_rank <= 20
ORDER BY rc.lifetime_value DESC;