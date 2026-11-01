from edgar import set_identity, Company
from config import MY_EMAIL


def _get_financials(ticker: str):
    if not MY_EMAIL:
        raise ValueError("MY_EMAIL is required for SEC EDGAR identity")
    set_identity(MY_EMAIL)
    return Company(ticker).get_financials()


def fetch_income_statement(ticker: str):
    financials = _get_financials(ticker)
    return financials.income_statement().to_dataframe()


def fetch_balance_sheet(ticker: str):
    financials = _get_financials(ticker)
    return financials.balance_sheet().to_dataframe()


def fetch_cash_flow_statement(ticker: str):
    financials = _get_financials(ticker)
    return financials.cash_flow_statement().to_dataframe()



if __name__ == "__main__":
    ticker = "AAPL"
    income_statement = fetch_income_statement(ticker)
    income_statement.to_csv(f"{ticker}_income_statement.csv")