from job.daily.ticker import update_universe
from job.daily.daily_data import run_daily_candle_jobs
from job.daily.pit_market_cap import update_pit_market_cap
import schedule
import time


def daily_tasks():
    update_universe()

    update_pit_market_cap()
    
    run_daily_candle_jobs()


def job():
    # schedule the daily jobs
    schedule.every().day.at("19:00", "America/New_York").do(daily_tasks)

    print("Scheduled daily jobs at 19:00 America/New_York")