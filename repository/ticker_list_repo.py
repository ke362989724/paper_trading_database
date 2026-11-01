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
        # 1. Set all tickers to inactive initially
        session.query(Ticker).update({Ticker.is_active: False})
        
        processed_count = 0
        for _, row in universe_df.iterrows():
            ticker_value = str(row["Ticker"]).strip()
            existing = session.query(Ticker).filter(Ticker.ticker == ticker_value).first()
            
            if existing:
                # Reactivate and update attributes if present in the current universe
                existing.is_active = True
                existing.name = str(row["Name"]).strip()
                existing.is_etf = bool(row["ETF"])
            else:
                # Add new record
                session.add(
                    Ticker(
                        name=str(row["Name"]).strip(),
                        ticker=ticker_value,
                        is_etf=bool(row["ETF"]),
                        is_active=True,
                    )
                )
                
            processed_count += 1

            if processed_count % batch_size == 0:
                session.commit()
                logger.info("Processed %s tickers so far", processed_count)

        session.commit()
        logger.info("Universe sync complete. Total processed: %s", processed_count)

    return processed_count


def fetch_active_us_universe() -> list[str]:
    with SessionLocal() as session:
        results = (
            session.query(Ticker.ticker)
            .filter(Ticker.is_active == True)
            .all()
        )
        data =  [r[0] for r in results]
        return data



def fetch_target_ticker(ticker: str) -> Ticker | None:
    with SessionLocal() as session:
        result = session.query(Ticker).filter(Ticker.ticker == ticker).first()
        id = result.id

        # Display it in a clean, tabular format
        return id
    