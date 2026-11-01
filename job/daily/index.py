from job.daily.ticker import update_universe
from job.daily.daily_data import run_daily_candle_jobs


def run_daily_jobs():
    update_universe()
    run_daily_candle_jobs()