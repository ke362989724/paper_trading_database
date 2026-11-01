import os
import pandas as pd
from edgar import set_identity, Company


def main():
    # 1. Set your SEC User-Agent identity
    set_identity("QuantPipeline your.email@example.com")

    # 2. Ticker universe to fetch
    tickers_universe = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
        'TSLA', 'NVDA', 'JPM', 'JNJ', 'V'
    ]

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    master_fundamental_database = {}

    for ticker in tickers_universe:
        print(f"[-] Fetching financials for: {ticker}...")
        try:
            company = Company(ticker)
            financials = company.get_financials()

            df_income = financials.income_statement().to_dataframe()
            df_balance = financials.balance_sheet().to_dataframe()
            df_cashflow = financials.cash_flow_statement().to_dataframe()

            master_fundamental_database[ticker] = {
                'income_statement': df_income,
                'balance_sheet': df_balance,
                'cash_flow': df_cashflow,
            }

            # Save each table to its own CSV file
            income_path = os.path.join(output_dir, f"{ticker}_income_statement.csv")
            balance_path = os.path.join(output_dir, f"{ticker}_balance_sheet.csv")
            cashflow_path = os.path.join(output_dir, f"{ticker}_cash_flow.csv")

            df_income.to_csv(income_path)
            df_balance.to_csv(balance_path)
            df_cashflow.to_csv(cashflow_path)

            print(f"[+] Successfully processed {ticker} and saved CSV files")

        except Exception as e:
            print(f"[!] Error processing {ticker}: {e}")

    # Show sample output if AAPL was processed
    if 'AAPL' in master_fundamental_database:
        print("\n=== Sample: AAPL Income Statement ===")
        print(master_fundamental_database['AAPL']['income_statement'].head())
        print("\n=== Sample: AAPL Balance Sheet ===")
        print(master_fundamental_database['AAPL']['balance_sheet'].head())
        print("\n=== Sample: AAPL Cash Flow Statement ===")
        print(master_fundamental_database['AAPL']['cash_flow'].head())

    print(f"\nAll CSV files saved in: {output_dir}")


if __name__ == "__main__":
    main()