from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import threading
import time

from repository.ticker_list_repo import fetch_active_us_universe, update_market_cap
from data_source.yahoo_finance_cap import fetch_market_cap

# Shared throttle: max ~2.5 req/sec across all threads
_throttle_lock = threading.Lock()
_next_allowed_time = 0.0
MIN_REQUEST_INTERVAL = 0.4  # seconds

RATE_LIMIT_MARKERS = ("Too Many Requests", "429", "rate limited")


def throttled_fetch_market_cap(ticker: str):
    global _next_allowed_time

    with _throttle_lock:
        now = time.monotonic()
        wait_s = _next_allowed_time - now
        if wait_s > 0:
            time.sleep(wait_s)
        _next_allowed_time = time.monotonic() + MIN_REQUEST_INTERVAL

    return fetch_market_cap(ticker)


def fetch_with_retry(ticker: str, max_attempts: int = 5):
    for attempt in range(1, max_attempts + 1):
        try:
            return throttled_fetch_market_cap(ticker)
        except Exception as e:
            msg = str(e)
            is_rate_limited = any(m.lower() in msg.lower() for m in RATE_LIMIT_MARKERS)
            if not is_rate_limited or attempt == max_attempts:
                raise

            # Exponential backoff + jitter
            sleep_s = (2 ** attempt) + random.uniform(0, 0.7)
            time.sleep(sleep_s)

    return None


def update_pit_market_cap():
    active_tickers = fetch_active_us_universe()
    max_workers = 3  # keep low to avoid burst/rate-limit

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {
            executor.submit(fetch_with_retry, ticker): ticker
            for ticker in active_tickers
        }

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                market_cap = future.result()
                if market_cap is not None:
                    update_market_cap(ticker, market_cap)
                print(f"Updated PIT market cap for {ticker}: {market_cap}")
            except Exception as e:
                print(f"Error updating PIT market cap for {ticker}: {e}")