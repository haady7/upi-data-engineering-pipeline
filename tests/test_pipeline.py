import pytest

from src.generate import generate_transactions
from src.transform import transform_transactions


def test_generator_is_reproducible_and_unique():
    first = generate_transactions(100, seed=7)
    second = generate_transactions(100, seed=7)
    assert first.equals(second)
    assert first["transaction_id"].is_unique


def test_transform_creates_analytics_features():
    clean, quality = transform_transactions(generate_transactions(100, seed=5))
    assert quality["valid"] is True
    assert {"transaction_date", "transaction_hour", "amount_band"} <= set(clean.columns)
    assert clean["amount"].gt(0).all()


def test_transform_rejects_invalid_amount():
    raw = generate_transactions(10, seed=3)
    raw.loc[0, "amount"] = -1
    with pytest.raises(ValueError):
        transform_transactions(raw)
