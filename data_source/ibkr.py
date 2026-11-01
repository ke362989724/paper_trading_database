from ib_async import *
import time


ib = IB()

async def ensure_connected():
    if not ib.isConnected():
        print("Not connected. Connecting to IB Gateway...")
        try:
            # Connect to paper trading port
            await ib.connectAsync('127.0.0.1', 4002, clientId=1, timeout=10)
            print("Successfully connected!")
        except Exception as e:
            print(f"Connection failed: {e}")


