import pandas as pd

from logging_config import configure_logging
from repository.ticker_list_repo import save_us_universe_to_db_bulk

logger = configure_logging()


def fetch_us_universe() -> pd.DataFrame:
    # 1. Fetch NASDAQ-listed securities
    nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    df_nasdaq = pd.read_csv(nasdaq_url, sep="|")

    # 2. Fetch Other Exchange-listed securities (NYSE, AMEX, ARCA, BATS)
    other_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"
    df_other = pd.read_csv(other_url, sep="|")

    # Footer/Metadata Cleanup
    df_nasdaq = df_nasdaq.dropna(subset=['Symbol'])
    df_other = df_other.dropna(subset=['ACT Symbol'])

    df_nasdaq = df_nasdaq[~df_nasdaq['Symbol'].str.contains("File Creation Time", na=False)]
    df_other = df_other[~df_other['ACT Symbol'].str.contains("File Creation Time", na=False)]

    # Exclude test issues using explicit exchange column
    df_nasdaq = df_nasdaq[df_nasdaq['Test Issue'] == 'N']
    df_other = df_other[df_other['Test Issue'] == 'N']

    # Standardize column headers and retain ETF status column
    df_nasdaq = df_nasdaq[['Symbol', 'Security Name', 'ETF']].copy()
    df_nasdaq.rename(columns={'Symbol': 'Ticker', 'Security Name': 'Name'}, inplace=True)

    df_other = df_other[['ACT Symbol', 'Security Name', 'ETF']].copy()
    df_other.rename(columns={'ACT Symbol': 'Ticker', 'Security Name': 'Name'}, inplace=True)

    # Combine master list
    master_universe = pd.concat([df_nasdaq, df_other], ignore_index=True)

    # Clean text formatting
    master_universe['Ticker'] = master_universe['Ticker'].astype(str).str.strip()
    master_universe['Name'] = master_universe['Name'].astype(str).str.strip()

    # Map ETF string flag to boolean
    master_universe['ETF_bool'] = master_universe['ETF'].map({'Y': True, 'N': False})

    # Define regex pattern for non-common equity keywords to exclude
    exclude_name_pattern = (
        r'(?i)\b('
        r'warrant|warrants|rt|right|rights|unit|units|preferred|pref|'
        r'depositary|depository|ads|adr|note|notes|debenture|debentures|'
        r'bond|bonds|trust|acquisition|spac'
        r')\b'
    )

    # Condition 1: Keep any valid ETF
    is_etf = master_universe['ETF_bool'] == True

    # Condition 2: Keep only clean Common Stocks (ETF is False, passing name/ticker filters)
    is_common_stock = (
        (master_universe['ETF_bool'] == False) &
        ~master_universe['Name'].str.contains(exclude_name_pattern, regex=True, na=False) &
        ~master_universe['Ticker'].str.contains(r'[\.\-\/](W|WS|R|RT|U|P|PR|WS)$', regex=True, case=False) &
        ~master_universe['Ticker'].str.match(r'^[A-Z]{4}[WRUZ]$', na=False)
    )

    # Filter master universe to include ETFs + Common Stocks only
    master_universe = master_universe[is_etf | is_common_stock].copy()

    # Finalize dataframe columns and drop duplicates
    master_universe['ETF'] = master_universe['ETF_bool']
    master_universe = master_universe[['Ticker', 'Name', 'ETF']]
    master_universe = master_universe.drop_duplicates(subset=['Ticker'])

    logger.info("Fetched common stock & ETF universe with %s tickers", len(master_universe))
    return master_universe


def save_us_universe(universe_df: pd.DataFrame) -> int:
    inserted_count = save_us_universe_to_db_bulk(universe_df)
    logger.info("Saved %s new tickers to the database", inserted_count)
    return inserted_count

if __name__ == "__main__":
    logger.info("Starting ticker universe fetch")
    universe_df = fetch_us_universe()
    print(f"Fetched {len(universe_df)} tickers")