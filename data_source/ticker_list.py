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

    # Safer footer cleanup: Drop rows where 'Symbol' or 'ACT Symbol' is NaN or contains metadata strings
    df_nasdaq = df_nasdaq.dropna(subset=['Symbol'])
    df_other = df_other.dropna(subset=['ACT Symbol'])

    df_nasdaq = df_nasdaq[~df_nasdaq['Symbol'].str.contains("File Creation Time", na=False)]
    df_other = df_other[~df_other['ACT Symbol'].str.contains("File Creation Time", na=False)]

    # Standardize column headers
    df_nasdaq = df_nasdaq[['Symbol', 'Security Name', 'ETF']].copy()
    df_nasdaq.rename(columns={'Symbol': 'Ticker', 'Security Name': 'Name'}, inplace=True)

    df_other = df_other[['ACT Symbol', 'Security Name', 'ETF']].copy()
    df_other.rename(columns={'ACT Symbol': 'Ticker', 'Security Name': 'Name'}, inplace=True)

    # Combine both into a single master universe
    master_universe = pd.concat([df_nasdaq, df_other], ignore_index=True)

    # Filter and clean
    master_universe = master_universe[master_universe['ETF'].isin(['Y', 'N'])].copy()
    master_universe['Ticker'] = master_universe['Ticker'].astype(str).str.strip()
    master_universe['Name'] = master_universe['Name'].astype(str).str.strip()
    master_universe['ETF'] = master_universe['ETF'].map({'Y': True, 'N': False})
    master_universe = master_universe.drop_duplicates(subset=['Ticker'])

    logger.info("Fetched master universe with %s tickers", len(master_universe))
    return master_universe


def save_us_universe(universe_df: pd.DataFrame) -> int:
    inserted_count = save_us_universe_to_db_bulk(universe_df)
    logger.info("Saved %s new tickers to the database", inserted_count)
    return inserted_count

if __name__ == "__main__":
    logger.info("Starting ticker universe fetch")
    universe_df = fetch_us_universe()
    print(f"Fetched {len(universe_df)} tickers")