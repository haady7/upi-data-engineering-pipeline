CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    event_timestamp TIMESTAMPTZ NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_hour SMALLINT NOT NULL,
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    location TEXT NOT NULL,
    payment_type TEXT NOT NULL,
    merchant_category TEXT NOT NULL,
    amount NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    amount_band TEXT NOT NULL,
    is_synthetic_risk SMALLINT NOT NULL CHECK (is_synthetic_risk IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_fact_sender ON fact_transactions(sender_id);
CREATE INDEX IF NOT EXISTS idx_fact_location ON fact_transactions(location);
