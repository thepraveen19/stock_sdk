# Import the api_calls class from api_client
from api.api_client import api_calls
from logger import logger


# Create an instance of api_calls
my_object = api_calls()

# Call the fourth function
fyrs_client = my_object.login_fyers()
print(fyrs_client.get_profile())
