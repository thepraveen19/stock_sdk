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
# response = my_equity_data.get_equity_data("NSE:SBIN-EQ") not required taken care of in line 19(my_equity_data.create_historical_data_continuous("NSE:SBIN-EQ", 5))
# create historical data for the symbol
# my_equity_data.create_historical_data(interval is in seconds)
my_equity_data.create_historical_data_continuous(5)




