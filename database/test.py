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

# create instances of the CRUD classes
historical_data_crud = HistoricalDataCRUD()
stock_crud = StockCRUD(session)

eq_data = EquityData(api_obj)
eq_data.create_historical_data_continuous(interval_sec=60)  # fetch data every 60 seconds

