import numpy as np
import pandas as pd

CITIES = ["Mumbai", "Pune", "Bengaluru", "Delhi", "Hyderabad", "Chennai", "Ahmedabad"]
CATEGORIES = ["Grocery", "Food", "Travel", "Utilities", "Retail", "Entertainment"]
PAYMENT_TYPES = ["P2P", "P2M", "BillPayment", "Recharge"]


def generate_transactions(rows: int = 10_000, seed: int = 42) -> pd.DataFrame:
    """Generate deterministic fictional UPI-like transactions."""
    if rows < 1:
        raise ValueError("rows must be >= 1")

    rng = np.random.default_rng(seed)
    timestamps = (
        pd.Timestamp("2025-01-01", tz="UTC")
        + pd.to_timedelta(rng.integers(0, 90 * 86_400, size=rows), unit="s")
    )
    amounts = np.round(
        np.clip(rng.lognormal(mean=5.0, sigma=1.0, size=rows), 5, 100_000), 2
    )

    df = pd.DataFrame({
        "transaction_id": [f"TXN{i:09d}" for i in range(1, rows + 1)],
        "timestamp": timestamps,
        "sender_id": [f"U{x:06d}" for x in rng.integers(1, max(100, rows // 8), rows)],
        "receiver_id": [f"R{x:06d}" for x in rng.integers(1, max(80, rows // 10), rows)],
        "amount": amounts,
        "location": rng.choice(CITIES, size=rows),
        "device_id": [f"D{x:05d}" for x in rng.integers(1, max(50, rows // 15), rows)],
        "payment_type": rng.choice(PAYMENT_TYPES, size=rows, p=[0.48, 0.32, 0.12, 0.08]),
        "merchant_category": rng.choice(CATEGORIES, size=rows),
    })

    # Synthetic risk patterns make the pipeline useful for testing analytics.
    late_hour = df["timestamp"].dt.hour.between(0, 4).to_numpy()
    high_value = amounts > 25_000
    repeated_sender = df["sender_id"].duplicated(keep=False).to_numpy()
    rapid_repeat = repeated_sender & (rng.random(rows) < 0.10)
    risk_probability = np.where(high_value | late_hour | rapid_repeat, 0.28, 0.008)
    df["is_synthetic_risk"] = (rng.random(rows) < risk_probability).astype("int8")
    return df
