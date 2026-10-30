from repository.database import Ticker, get_engine, get_session_factory, init_db


def main() -> None:
    # Build engine from DATABASE_URL in .env
    engine = get_engine(echo=True)

    # Create tables (safe to call repeatedly)
    init_db(engine)

    # Create session factory
    SessionLocal = get_session_factory(engine)

    # Insert data
    with SessionLocal() as session:
        existing = session.query(Ticker).filter(Ticker.ticker == "AAPL").first()
        if existing:
            print("AAPL already exists, skipping insert.")
            return

        row = Ticker(name="Apple Inc.", ticker="AAPL", is_etf=False, is_active=True)
        session.add(row)
        session.commit()
        print(f"Inserted ticker with id={row.id}")


if __name__ == "__main__":
    main()