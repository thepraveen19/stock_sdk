# Import the api_calls class from api_client
from api.api_client import ApiCalls, EquityData
from logger import logger
import pandas as pd
from datetime import datetime


# Create an instance of api_calls
my_object = ApiCalls()

# Call the fourth function
fyrs_client = my_object.login_fyers()
# print(fyrs_client.get_profile())

my_equity_data = EquityData(fyrs_client)
response = my_equity_data.get_equity_data("NSE:SBIN-EQ,NSE:HDFC-EQ")

data = []
for stock in response['d']:
    stock_data = {}
    stock_data['id'] = stock['v']['fyToken']
    timestamp = datetime.fromtimestamp(stock['v']['tt'])
    stock_data['date'] = timestamp.strftime('%Y-%m-%d')
    stock_data['time'] = timestamp.strftime('%H:%M:%S')
    stock_data['stock_id'] = stock['n']
    stock_data['open_price'] = stock['v']['open_price']
    stock_data['high_price'] = stock['v']['high_price']
    stock_data['low_price'] = stock['v']['low_price']
    stock_data['close_price'] = stock['v']['lp']
    data.append(stock_data)

df = pd.DataFrame(data, columns=['id', 'date', 'time', 'stock_id', 'open_price', 'high_price', 'low_price', 'close_price'])
df.to_csv('testrun.csv')


# Extract the relevant data from the response dictionary
stock_data = response["d"][0]["v"]
stock_id = response["d"][0]["n"]
t = stock_data["cmd"]["t"]
date_time = pd.to_datetime(t, unit='s')
date = date_time.strftime('%Y-%m-%d')
time = date_time.strftime('%H:%M:%S')
open_price = stock_data["open_price"]
high_price = stock_data["high_price"]
low_price = stock_data["low_price"]
close_price = stock_data["c"]

# Create a DataFrame with the candlestick data
data = {
    "id": [stock_id],
    "date": [date],
    "time": [time],
    "open_price": [open_price],
    "high_price": [high_price],
    "low_price": [low_price],
    "close_price": [close_price],
}
df = pd.DataFrame(data)

# Print the DataFrame
print(df)