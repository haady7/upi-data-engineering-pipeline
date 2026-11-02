import argparse
import json
import logging

from config.settings import DATABASE_URL, PROCESSED_DIR, RAW_DIR, REPORTS_DIR
from .generate import generate_transactions
from .load import load_to_postgres
from .transform import transform_transactions

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run(rows: int = 10_000, seed: int = 42, load_db: bool = False) -> dict:
    logger.info("Generating %s synthetic transactions", rows)
    raw = generate_transactions(rows=rows, seed=seed)
    raw.to_csv(RAW_DIR / "upi_transactions.csv", index=False)

    clean, quality = transform_transactions(raw)
    clean.to_parquet(PROCESSED_DIR / "upi_transactions.parquet", index=False)
    (REPORTS_DIR / "data_quality.json").write_text(
        json.dumps(quality, indent=2), encoding="utf-8"
    )

    loaded = 0
    if load_db:
        if not DATABASE_URL:
            raise RuntimeError("Set DATABASE_URL in .env (see .env.example)")
        loaded = load_to_postgres(clean, DATABASE_URL)

    summary = {
        "generated_rows": len(raw),
        "processed_rows": len(clean),
        "loaded_rows": loaded,
        "seed": seed,
        "quality": quality,
        "database_loaded": bool(load_db),
    }
    (REPORTS_DIR / "pipeline_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    logger.info("Pipeline complete: %s", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the synthetic UPI data pipeline")
    parser.add_argument("--rows", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--load-db", action="store_true")
    arguments = parser.parse_args()
    run(arguments.rows, arguments.seed, arguments.load_db)
