from datetime import datetime
from time import sleep

import pandas as pd

from api_client import EquityData
from database.database import Session
from database.models import HistoricalData, Stock


class HistoricalDataLoader:
    def __init__(self, interval=300):
        self.session = Session()
        self.equity_data = EquityData()
        self.interval = interval
    
    def load_historical_data(self):
        while True:
            # Query the database to get a list of all stock symbols
            stocks = self.session.query(Stock.symbol).all()
            symbols = [stock[0] for stock in stocks]

            # Fetch the equity data for each symbol and insert it into the historical_data table
            for symbol in symbols:
                response = self.equity_data.get_equity_data(symbol)
                df = self.equity_data.create_stock_data_df(response)
                self.insert_historical_data(df)

            # Sleep for the specified interval before fetching data again
            sleep(self.interval)

    def insert_historical_data(self, df):
        for index, row in df.iterrows():
            historical_data = HistoricalData(
                stock_id=row['stock_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(row['time'], '%H:%M:%S').time(),
                open_price=row['open_price'],
                high_price=row['high_price'],
                low_price=row['low_price'],
                close_price=row['close_price']
            )
            self.session.add(historical_data)
        self.session.commit()
