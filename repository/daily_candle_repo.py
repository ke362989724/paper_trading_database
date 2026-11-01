import pandas as pd

from logging_config import configure_logging
from repository.database import SessionLocal, Ticker
from repository.ticker_list_repo import fetch_target_ticker
from sqlalchemy.dialects.postgresql import insert
from repository.models import DailyCandle

logger = configure_logging()


def save_daily_candles(ticker, daily_candles) -> int:
    if daily_candles is None or daily_candles.empty:
        return 0

    ticker_id = fetch_target_ticker(ticker)
    data_list = []

    for _, candle in daily_candles.iterrows():
        data_list.append(
            {
                "ticker_id": ticker_id,
                "timestamp": pd.to_datetime(candle["date"]),
                "open": float(candle["open"]),
                "high": float(candle["high"]),
                "low": float(candle["low"]),
                "close": float(candle["close"]),
                "volume": float(candle["volume"]),
            }
        )

    if not data_list:
        return 0

    stmt = insert(DailyCandle).values(data_list)
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=["ticker_id", "timestamp"],
        set_={
            "open": stmt.excluded.open,
            "high": stmt.excluded.high,
            "low": stmt.excluded.low,
            "close": stmt.excluded.close,
            "volume": stmt.excluded.volume,
        }
    )

    with SessionLocal() as session:
        result = session.execute(upsert_stmt)
        session.commit()
        return result.rowcount
        
        
    