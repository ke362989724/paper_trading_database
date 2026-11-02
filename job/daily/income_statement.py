from data_source.edgar_income_statement import fetch_revenue_and_net_income_by_year
from data_source.edgar_income_statement import save_income_statement
from repository.ticker_list_repo import fetch_active_us_universe
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def _process_one_ticker(ticker: str):
    started = time.perf_counter()
    try:
        revenue_and_net_income = fetch_revenue_and_net_income_by_year(ticker)
        save_income_statement(ticker, revenue_and_net_income)
        return {"ticker": ticker, "ok": True, "error": None, "sec": time.perf_counter() - started}
    except Exception as exc:
        return {"ticker": ticker, "ok": False, "error": str(exc), "sec": time.perf_counter() - started}

def fetch_and_save_income_statement_concurrent(max_workers: int = 4):
    ticker_lists = fetch_active_us_universe()
    total = len(ticker_lists)
    ok = 0
    fail = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_one_ticker, ticker): ticker for ticker in ticker_lists}

        for i, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            if result["ok"]:
                ok += 1
                print(f"[{i}/{total}] OK {result['ticker']} {result['sec']:.2f}s")
            else:
                fail += 1
                print(f"[{i}/{total}] FAIL {result['ticker']} {result['sec']:.2f}s - {result['error']}")

    print(f"Done. success={ok}, failed={fail}, total={total}")