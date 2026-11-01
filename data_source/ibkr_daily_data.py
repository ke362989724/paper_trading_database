from data_source.ibkr import ensure_connected, ib, Stock, util



async def fetch_single_daily_data(symbol):
    contract = Stock(symbol, 'SMART', 'USD')
    try:
        bars = await ib.reqHistoricalDataAsync(
            contract,
            endDateTime='',
            durationStr='2 Y',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1,
        )
        df = util.df(bars)
        return df
    except Exception as e:
        print(f"Failed to fetch daily data for {symbol}: {e}")
        return None
