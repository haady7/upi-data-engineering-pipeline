import pandas as pd

REQUIRED = [
    "transaction_id", "timestamp", "sender_id", "receiver_id", "amount",
    "location", "device_id", "payment_type", "merchant_category", "is_synthetic_risk",
]


def validate_transactions(df: pd.DataFrame) -> dict:
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    numeric_amount = pd.to_numeric(df["amount"], errors="coerce")
    report = {
        "row_count": int(len(df)),
        "duplicate_transaction_ids": int(df["transaction_id"].duplicated().sum()),
        "null_cells": int(df[REQUIRED].isna().sum().sum()),
        "invalid_amounts": int((numeric_amount.isna() | (numeric_amount <= 0)).sum()),
        "invalid_risk_labels": int((~df["is_synthetic_risk"].isin([0, 1])).sum()),
    }
    report["valid"] = all(
        report[key] == 0 for key in (
            "duplicate_transaction_ids", "null_cells", "invalid_amounts", "invalid_risk_labels"
        )
    )
    return report
