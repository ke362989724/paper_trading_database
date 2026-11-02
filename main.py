from repository.database import init_db
from repository.models import Ticker
from sqlalchemy import select
import pandas as pd
from data_source.ticker_list import fetch_us_universe, save_us_universe
from repository.ticker_list_repo import fetch_active_us_universe, fetch_target_ticker, update_market_cap
from repository.daily_candle_repo import save_daily_candles
import asyncio
from edgar import set_identity, Company
from job.daily.income_statement import fetch_and_save_income_statement_concurrent
from data_source.yahoo_finance_cap import fetch_market_cap
from job.daily.index import daily_tasks, job
import schedule
import time


def main():
    print("Running scheduled daily jobs")
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    init_db()
    main()
