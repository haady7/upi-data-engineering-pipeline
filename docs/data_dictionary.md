# Data dictionary

| Field | Meaning |
|---|---|
| transaction_id | Unique fictional transaction key |
| timestamp | UTC event timestamp |
| sender_id / receiver_id | Fictional account identifiers |
| amount | Positive synthetic transaction amount |
| location | Synthetic city label |
| device_id | Fictional device identifier |
| payment_type | P2P, P2M, bill payment or recharge |
| merchant_category | Fictional category |
| is_synthetic_risk | Generator-created 0/1 risk flag, not ground truth |
| transaction_date | Derived UTC date |
| transaction_hour | Derived UTC hour |
| amount_band | Derived low / medium / high / very_high bucket |

No real customer, bank, phone, UPI or payment information is included.
