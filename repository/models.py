from repository.database import Base
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, func, UniqueConstraint
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