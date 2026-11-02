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
from job.daily.income_statement import fetch_and_save_income_statement_concurrent
from data_source.yahoo_finance_cap import fetch_market_cap


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)


    ticker = "AAPL"
    market_cap = fetch_market_cap(ticker)
    print(f"{ticker} market cap = {market_cap:,} USD" if market_cap else "market cap not available")