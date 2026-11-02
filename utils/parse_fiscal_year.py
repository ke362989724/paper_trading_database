import pandas as pd

def parse_fiscal_year_columns(raw_fiscal_year_columns):
    clean_fiscal_year_columns = [c.replace(" (FY)", "") for c in raw_fiscal_year_columns]
    
    parsed_fiscal_year_columns = pd.to_datetime(
        clean_fiscal_year_columns,
        format="%Y-%m-%d",
        errors="raise",
    ).date
    
    return parsed_fiscal_year_columns