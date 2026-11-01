from edgar import set_identity, Company
import pandas as pd
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

def fetch_revenue_and_net_income_by_year(ticker: str):
    income_statement = fetch_income_statement(ticker)
    # save the raw income statement to a CSV file for reference
    print(income_statement)
    
    if income_statement.empty:
        raise ValueError(f"No income statement data found for {ticker}")
        
    fiscal_year_columns = [column for column in income_statement.columns if "(FY)" in column]

    # Helper function to safely fetch row values or return None if missing
    def get_row_values(concept_name):
        row = income_statement[income_statement["standard_concept"].str.strip().str.lower() == concept_name]
        if row.empty:
            print(f"⚠️ Warning: Concept '{concept_name}' not found for {ticker}. Filling with NaN.")
            return [None] * len(fiscal_year_columns)
        return row.iloc[0][fiscal_year_columns].values

    # Build DataFrame safely using the helper
    result_df = pd.DataFrame(
        {
            "fiscal_year": fiscal_year_columns,
            "revenue": get_row_values("revenue"),
            "net_income": get_row_values("netincome"),
            "operating_income": get_row_values("operatingincomeloss"),
            "gross_profit": get_row_values("grossprofit"),
            "cost_of_goods_sold": get_row_values("costofgoodsandservicessold"),
        }
    )
    
    # Convert columns to numeric safely
    numeric_cols = ["revenue", "net_income", "operating_income", "gross_profit", "cost_of_goods_sold"]
    for col in numeric_cols:
        result_df[col] = pd.to_numeric(result_df[col], errors="coerce")
    return result_df


if __name__ == "__main__":
    for ticker in ["NVDA"]:
        revenue_and_net_income = fetch_revenue_and_net_income_by_year(ticker)
        print(revenue_and_net_income.to_string(index=False))