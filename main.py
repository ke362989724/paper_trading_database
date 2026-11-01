from repository.database import engine, Base, SessionLocal
from repository.models import Ticker
from sqlalchemy import select
import pandas as pd
from data_source.ticker_list import fetch_us_universe, save_us_universe
from job.daily.index import run_daily_jobs
from repository.ticker_list_repo import fetch_active_us_universe, fetch_target_ticker
from repository.daily_candle_repo import save_daily_candles
import asyncio
from edgar import set_identity, Company


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)