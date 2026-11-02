-- Daily transaction volume and value
SELECT transaction_date, COUNT(*) AS transactions, ROUND(SUM(amount), 2) AS total_value
FROM fact_transactions
GROUP BY transaction_date
ORDER BY transaction_date;

-- City activity and synthetic-risk share
SELECT location, COUNT(*) AS transactions,
       ROUND(AVG(is_synthetic_risk::numeric) * 100, 2) AS synthetic_risk_pct
FROM fact_transactions
GROUP BY location
ORDER BY transactions DESC;

-- Payment type mix
SELECT payment_type, COUNT(*) AS transactions, ROUND(SUM(amount), 2) AS total_value
FROM fact_transactions
GROUP BY payment_type
ORDER BY transactions DESC;

-- Hourly activity profile
SELECT transaction_hour, COUNT(*) AS transactions, ROUND(AVG(amount), 2) AS avg_amount
FROM fact_transactions
GROUP BY transaction_hour
ORDER BY transaction_hour;

-- Frequent senders for operational review
SELECT sender_id, COUNT(*) AS transactions, ROUND(SUM(amount), 2) AS total_value
FROM fact_transactions
GROUP BY sender_id
HAVING COUNT(*) >= 10
ORDER BY transactions DESC
LIMIT 25;

-- Synthetic risk review queue: never treat this generated label as a real fraud decision
SELECT transaction_id, event_timestamp, sender_id, receiver_id, amount, location, device_id
FROM fact_transactions
WHERE is_synthetic_risk = 1
ORDER BY amount DESC
LIMIT 100;
