from repository.models import Ticker, DailyCandle
from sqlalchemy import select
import pandas as pd
from data_source.ticker_list import fetch_us_universe, save_us_universe



def update_universe():
    universe_df = fetch_us_universe()
    inserted_count = save_us_universe(universe_df)
    print(f"Fetched {len(universe_df)} tickers")
    print(f"Saved {inserted_count} new tickers to the database")