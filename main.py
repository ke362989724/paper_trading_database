from repository.database import engine, Base, SessionLocal
from repository.models import Ticker
from sqlalchemy import select
import pandas as pd
from data_source.ticker_list import fetch_us_universe, save_us_universe
from job.daily.index import run_daily_jobs


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    
    run_daily_jobs()
