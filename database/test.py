from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import HistoricalData, Stock
from crud import HistoricalDataCRUD, StockCRUD
import pandas as pd
from database import engine, Session
from apiclient import EquityData

import pandas as pd
from datetime import datetime
# create a database session
Session = sessionmaker(bind=engine)
session = Session()
EquityData = EquityData()
# create instances of the CRUD classes
historical_data_crud = HistoricalDataCRUD()
stock_crud = StockCRUD(session)



# create an instance of the EquityData class
equity_data = EquityData(api_client)

# call the get_equity_data method to get data for a symbol
symbol = 'AAPL'
data = EquityData.get_equity_data(symbol)

# create historical data for the symbol
equity_data.create_historical_data(symbol)