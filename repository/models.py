from repository.database import Base
from datetime import datetime
from sqlalchemy import Date, Boolean, DateTime, Float, ForeignKey, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Ticker(Base):
    __tablename__ = "tickers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ticker: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    is_etf: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship back to DailyCandle (optional, but recommended)
    candles: Mapped[list["DailyCandle"]] = relationship(
        back_populates="ticker_rel", cascade="all, delete-orphan"
    )


class DailyCandle(Base):
    __tablename__ = "daily_candles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    ticker_id: Mapped[int] = mapped_column(ForeignKey("tickers.id"), nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ticker_rel: Mapped["Ticker"] = relationship(back_populates="candles")

    # Corrected from __table__args__ to __table_args__
    __table_args__ = (
        UniqueConstraint("ticker_id", "timestamp", name="uix_ticker_timestamp"),
    )

class IncomeStatement(Base):
    __tablename__ = "income_statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker_id: Mapped[int] = mapped_column(ForeignKey("tickers.id"), nullable=False)
    revenue: Mapped[float] = mapped_column(Float, nullable=False)
    cost_of_goods_sold: Mapped[float] = mapped_column(Float, nullable=False)
    gross_profit: Mapped[float] = mapped_column(Float, nullable=False)
    operating_expenses: Mapped[float] = mapped_column(Float, nullable=False)
    operating_income: Mapped[float] = mapped_column(Float, nullable=False)
    net_income: Mapped[float] = mapped_column(Float, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(Date, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ticker_rel: Mapped["Ticker"] = relationship(back_populates="income_statements")

    __table_args__ = (
        UniqueConstraint("ticker_id", "fiscal_year", name="uix_ticker_fiscal_year"),
    )

class BalanceSheet(Base):
    __tablename__ = "balance_sheets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker_id: Mapped[int] = mapped_column(ForeignKey("tickers.id"), nullable=False)
    total_assets: Mapped[float] = mapped_column(Float, nullable=False)
    total_liabilities: Mapped[float] = mapped_column(Float, nullable=False)
    equity: Mapped[float] = mapped_column(Float, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(Date, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ticker_rel: Mapped["Ticker"] = relationship(back_populates="balance_sheets")

    __table_args__ = (
        UniqueConstraint("ticker_id", "fiscal_year", name="uix_ticker_fiscal_year"),
    )

class CashFlowStatement(Base):
    __tablename__ = "cash_flow_statements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker_id: Mapped[int] = mapped_column(ForeignKey("tickers.id"), nullable=False)
    operating_cash_flow: Mapped[float] = mapped_column(Float, nullable=False)
    investing_cash_flow: Mapped[float] = mapped_column(Float, nullable=False)
    financing_cash_flow: Mapped[float] = mapped_column(Float, nullable=False)
    fiscal_year: Mapped[int] = mapped_column(Date, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    ticker_rel: Mapped["Ticker"] = relationship(back_populates="cash_flow_statements")

    __table_args__ = (
        UniqueConstraint("ticker_id", "fiscal_year", name="uix_ticker_fiscal_year"),
    )