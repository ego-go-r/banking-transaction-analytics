SELECT
    COUNT(*) AS transactions,
    ROUND(SUM(amount), 2) AS total_volume,
    ROUND(AVG(amount), 2) AS average_transaction
FROM transactions;


SELECT
    category,
    COUNT(*) AS transactions,
    ROUND(SUM(amount), 2) AS total_volume,
    ROUND(AVG(amount), 2) AS average_transaction
FROM transactions
GROUP BY category
ORDER BY total_volume DESC;


SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*) AS transactions,
    ROUND(SUM(amount), 2) AS total_volume
FROM transactions
GROUP BY month
ORDER BY month;


SELECT
    c.region,
    COUNT(t.transaction_id) AS transactions,
    ROUND(SUM(t.amount), 2) AS total_volume,
    ROUND(AVG(t.amount), 2) AS average_transaction
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_volume DESC;



SELECT
    customer_id,
    COUNT(*) AS transactions,
    ROUND(SUM(amount), 2) AS total_spent,
    ROUND(AVG(amount), 2) AS average_transaction
FROM transactions
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 20;


SELECT
    ROUND(
        SUM(
            CASE
                WHEN is_fraud = 1
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate
FROM transactions;


SELECT
    category,

    COUNT(*) AS transactions,

    SUM(
        CASE
            WHEN is_fraud = 1
            THEN 1
            ELSE 0
        END
    ) AS fraud_transactions,

    ROUND(
        SUM(
            CASE
                WHEN is_fraud = 1
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate

FROM transactions

GROUP BY category

ORDER BY fraud_rate DESC;



SELECT

    customer_id,

    COUNT(*) AS transactions,

    ROUND(
        SUM(amount),
        2
    ) AS total_spent,

    SUM(
        CASE
            WHEN is_fraud = 1
            THEN 1
            ELSE 0
        END
    ) AS fraud_transactions

FROM transactions

GROUP BY customer_id

HAVING fraud_transactions > 0

ORDER BY fraud_transactions DESC;


SELECT
    transaction_id,
    customer_id,
    transaction_date,
    category,
    amount
FROM transactions
WHERE amount > 1000
ORDER BY amount DESC;



SELECT
    transaction_id,
    customer_id,
    transaction_date,
    category,
    amount
FROM transactions
WHERE is_fraud = 1
ORDER BY amount DESC;