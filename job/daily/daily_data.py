from repository.models import Ticker, DailyCandle
from sqlalchemy import select
import pandas as pd
from data_source.ticker_list import fetch_us_universe, save_us_universe
from repository.ticker_list_repo import fetch_active_us_universe, fetch_target_ticker
from repository.daily_candle_repo import save_daily_candles
from data_source.ibkr_daily_data import fetch_single_daily_data
from data_source.ibkr import ensure_connected
import asyncio



def fetch_and_save_us_universe():
    us_universe = fetch_us_universe()
    save_us_universe(us_universe)
    return us_universe


async def fetch_and_save_daily_data(batch_size=5, delay=2):
    active_tickers = fetch_active_us_universe()
    active_tickers_len = len(active_tickers)
    await ensure_connected()
    for i in range(0, active_tickers_len, batch_size):
        batch = active_tickers[i:i+batch_size]
        print(f"Fetching batch: {batch}")

        # Create asynchronous tasks for current batch
        tasks = [fetch_single_daily_data(ticker) for ticker in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for ticker, daily_data in zip(batch, results):
            if isinstance(daily_data, Exception):
                print(f"Error fetching data for {ticker}: {daily_data}")
                continue
            if daily_data is not None and not daily_data.empty:
                save_daily_candles(ticker, daily_data)
        await asyncio.sleep(delay)


def run_daily_candle_jobs():
    asyncio.run(fetch_and_save_daily_data())