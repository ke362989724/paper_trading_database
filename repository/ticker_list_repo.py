import pandas as pd

from logging_config import configure_logging
from repository.database import SessionLocal, Ticker

logger = configure_logging()


def save_us_universe_to_db_bulk(
    universe_df: pd.DataFrame | None = None,
    *,
    batch_size: int = 500,
) -> int:
    if universe_df is None:
        raise ValueError("universe_df cannot be None")

    inserted = 0

    with SessionLocal() as session:
        for _, row in universe_df.iterrows():
            ticker_value = str(row["Ticker"]).strip()
            existing = session.query(Ticker).filter(Ticker.ticker == ticker_value).first()
            if existing:
                continue

            session.add(
                Ticker(
                    name=str(row["Name"]).strip(),
                    ticker=ticker_value,
                    is_etf=bool(row["ETF"]),
                    is_active=True,
                )
            )
            inserted += 1

            if inserted % batch_size == 0:
                session.commit()
                logger.info("Committed %s tickers so far", inserted)

        session.commit()

    logger.info("Saved %s new tickers to the database", inserted)
    return inserted