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





