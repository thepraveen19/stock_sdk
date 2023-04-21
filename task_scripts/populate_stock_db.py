import sys
sys.path.append('/Users/praveenkadam/Documents/Algorithmic_trading/stock_sdk')
from database.database import Session
from database.models import Stock
import time

from database.database import Session
from database.models import Stock

class StockLoader:
    def __init__(self):
        self.session = Session()
        
    def load_stocks(self, stock_data):
        # iterate through each row of the stock_data DataFrame and create a new Stock object for each
        for index, row in stock_data.iterrows():
            stock = Stock(name=row['name'], symbol=row['symbol'], description=row['description'])
            self.session.add(stock)

        # commit the changes to the database
        self.session.commit()

class StockDeleter: # NEVER USE THIS - IF YOU WISH TO, YOU MUST KNOW WHAT YOU ARE DOING
    def __init__(self):
        self.session = Session()
        
    def delete_all_stocks(self):
        # delete all the stocks in the database
        self.session.query(Stock).delete()
        
        # commit the changes to the database
        self.session.commit()

loader = StockLoader()
deleter = StockDeleter()

# Example usage with a DataFrame
import pandas as pd
# Get a csv file from which the list of stocks can be retrived in the df.
# this can be loaded as below. As of now in the next line stock_data is loading a few stock names in the stocks table.
# replace stock_data = pd.dataframe..... by pd.read csv.. the last line remains untouched.
# stock_data = pd.DataFrame({
#     'name': ['Reliance Industries Ltd.', 'HDFC Bank Ltd.', 'Infosys Ltd.'],
#     'symbol': ['RELIANCE.NS', 'HDFCBANK.EQ', 'INFY.NS'],
#     'description': ['Diversified conglomerate in India', 'Indian banking and financial services company', 'Indian multinational information technology company']
# })

stock_data = pd.read_csv(r"/Users/praveenkadam/Documents/Algorithmic_trading/stock_sdk/fo_mktlots.csv")
loader.load_stocks(stock_data)

