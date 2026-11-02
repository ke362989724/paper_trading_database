import pandas as pd

from logging_config import configure_logging
from repository.database import SessionLocal, Ticker
from repository.ticker_list_repo import fetch_target_ticker
from sqlalchemy.dialects.postgresql import insert
from repository.models import DailyCandle
from repository.models import IncomeStatement

logger = configure_logging()


def save_income_statement(ticker, income_statement_data) -> int:
    if income_statement_data is None or income_statement_data.empty:
        return 0

    ticker_id = fetch_target_ticker(ticker)
    data_list = []

    for _, row in income_statement_data.iterrows():
        data_list.append(
            {
                "ticker_id": ticker_id,
                "fiscal_year": pd.to_datetime(row["fiscal_year"]),
                "revenue": float(row["revenue"]) if row["revenue"] is not None else None,
                "cost_of_goods_sold": float(row["cost_of_goods_sold"]) if row["cost_of_goods_sold"] is not None else None,
                "gross_profit": float(row["gross_profit"]) if row["gross_profit"] is not None else None,
                "operating_income": float(row["operating_income"]) if row["operating_income"] is not None else None,
                "net_income": float(row["net_income"]) if row["net_income"] is not None else None,
            }
        )

    if not data_list:
        return 0

    stmt = insert(IncomeStatement).values(data_list)
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=["ticker_id", "fiscal_year"],
        set_={
            "revenue": stmt.excluded.revenue,
            "cost_of_goods_sold": stmt.excluded.cost_of_goods_sold,
            "gross_profit": stmt.excluded.gross_profit,
            "operating_income": stmt.excluded.operating_income,
            "net_income": stmt.excluded.net_income,
        }
    )

    with SessionLocal() as session:
        result = session.execute(upsert_stmt)
        session.commit()
        return result.rowcount
        
    