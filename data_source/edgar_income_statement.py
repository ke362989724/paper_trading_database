import pandas as pd
from repository.income_statement_repo import save_income_statement
from data_source.edgar import _get_financials
from utils.parse_fiscal_year import parse_fiscal_year_columns



def fetch_income_statement(ticker: str):
    financials = _get_financials(ticker)
    if financials is None:
        raise ValueError(f"No financials returned by EDGAR for {ticker}")

    income_statement = financials.income_statement()
    if income_statement is None:
        raise ValueError(f"No income statement returned by EDGAR for {ticker}")

    return income_statement.to_dataframe()

def fetch_income_statement_by_year(ticker: str):
    income_statement = fetch_income_statement(ticker)
    # save the raw income statement to a CSV file for reference
    
    if income_statement.empty:
        raise ValueError(f"No income statement data found for {ticker}")
        
    raw_fiscal_year_columns = [c for c in income_statement.columns if "(FY)" in c]
    parsed_fiscal_year_columns = parse_fiscal_year_columns(raw_fiscal_year_columns)


    # Helper function to safely fetch row values or return None if missing
    def get_row_values(concept_name):
        row = income_statement[income_statement["standard_concept"].str.strip().str.lower() == concept_name]
        if row.empty:
            print(f"⚠️ Warning: Concept '{concept_name}' not found for {ticker}. Filling with NaN.")
            return [None] * len(raw_fiscal_year_columns)
        return row.iloc[0][raw_fiscal_year_columns].values

    # Build DataFrame safely using the helper
    result_df = pd.DataFrame(
        {
            "fiscal_year": parsed_fiscal_year_columns,
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
        revenue_and_net_income = fetch_income_statement_by_year(ticker)
        save_income_statement(ticker, revenue_and_net_income)
        print("finished fetching and saving income statement for", ticker)