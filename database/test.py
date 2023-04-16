from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import HistoricalData, Stock
from crud import HistoricalDataCRUD, StockCRUD
import pandas as pd
from database import engine, Session
 
import pandas as pd
from datetime import datetime
# create a database session
Session = sessionmaker(bind=engine)
session = Session()

# create instances of the CRUD classes
historical_data_crud = HistoricalDataCRUD()
stock_crud = StockCRUD(session)

historical_data = historical_data_crud.create_historical_data(timestamp='01:01:00', stock_id='123', open_price=100,
                                                                  high_price=120, low_price=22,
                                                                  close_price=113, volume=222222)


# read the data into a pandas dataframe
df = pd.read_csv('testrun.csv', parse_dates=[['date', 'time']])

# iterate through the rows of the dataframe and create HistoricalData objects
for index, row in df.iterrows():
    stock_id = row['stock_id']
    stock = stock_crud.read_stock(stock_id)
    timestamp = row['date_time']
    open_price = row['open_price']
    high_price = row['high_price']
    low_price = row['low_price']
    close_price = row['close_price']
    volume = row['volume']
    historical_data = historical_data_crud.create_historical_data(timestamp=timestamp, stock_id=stock, open_price=open_price,
                                                                  high_price=high_price, low_price=low_price,
                                                                  close_price=close_price, volume=volume)

