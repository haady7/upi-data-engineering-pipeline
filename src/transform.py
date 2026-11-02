import pandas as pd
from .quality import validate_transactions


def transform_transactions(df: pd.DataFrame):
    quality = validate_transactions(df)
    if not quality["valid"]:
        raise ValueError(f"Data quality checks failed: {quality}")

    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="raise")
    out["amount"] = pd.to_numeric(out["amount"], errors="raise").round(2)

    text_columns = [
        "transaction_id", "sender_id", "receiver_id", "device_id", "location",
        "payment_type", "merchant_category",
    ]
    for column in text_columns:
        out[column] = out[column].astype("string").str.strip()

    out["transaction_date"] = out["timestamp"].dt.date.astype("string")
    out["transaction_hour"] = out["timestamp"].dt.hour.astype("int8")
    out["amount_band"] = pd.cut(
        out["amount"],
        bins=[0, 500, 2_000, 10_000, float("inf")],
        labels=["low", "medium", "high", "very_high"],
        include_lowest=True,
    ).astype("string")
    return out, quality
