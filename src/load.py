import pandas as pd
from sqlalchemy import create_engine, text

DDL = """
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
"""


def load_to_postgres(df: pd.DataFrame, database_url: str) -> int:
    engine = create_engine(database_url, pool_pre_ping=True)
    records = df.rename(columns={"timestamp": "event_timestamp"})[[
        "transaction_id", "event_timestamp", "transaction_date", "transaction_hour",
        "sender_id", "receiver_id", "device_id", "location", "payment_type",
        "merchant_category", "amount", "amount_band", "is_synthetic_risk",
    ]]

    try:
        with engine.begin() as connection:
            for statement in DDL.split(";"):
                if statement.strip():
                    connection.execute(text(statement))

            records.to_sql("stg_transactions", connection, if_exists="replace", index=False)
            connection.execute(text("""
                INSERT INTO fact_transactions (
                    transaction_id, event_timestamp, transaction_date, transaction_hour,
                    sender_id, receiver_id, device_id, location, payment_type,
                    merchant_category, amount, amount_band, is_synthetic_risk
                )
                SELECT transaction_id, event_timestamp, transaction_date::date, transaction_hour,
                       sender_id, receiver_id, device_id, location, payment_type,
                       merchant_category, amount, amount_band, is_synthetic_risk
                FROM stg_transactions
                ON CONFLICT (transaction_id) DO UPDATE SET
                    event_timestamp = EXCLUDED.event_timestamp,
                    transaction_date = EXCLUDED.transaction_date,
                    transaction_hour = EXCLUDED.transaction_hour,
                    sender_id = EXCLUDED.sender_id,
                    receiver_id = EXCLUDED.receiver_id,
                    device_id = EXCLUDED.device_id,
                    location = EXCLUDED.location,
                    payment_type = EXCLUDED.payment_type,
                    merchant_category = EXCLUDED.merchant_category,
                    amount = EXCLUDED.amount,
                    amount_band = EXCLUDED.amount_band,
                    is_synthetic_risk = EXCLUDED.is_synthetic_risk
            """))
            connection.execute(text("DROP TABLE stg_transactions"))
    finally:
        engine.dispose()

    return len(records)
