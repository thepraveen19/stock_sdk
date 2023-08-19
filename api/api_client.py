import os
import sys

# Add the desired path to the sys.path list
desired_path = "/Users/praveenkadam/Documents/Algorithmic_trading 2/temp_env/lib/python3.11/site-packages"
sys.path.append(desired_path)

from stock_sdk.api import *
from stock_sdk.api.endpoints import *
from stock_sdk.config import *
from stock_sdk.credentials import *
import requests
import json
import time
import pyotp
import os
from urllib.parse import parse_qs, urlparse
import sys
from fyers_apiv3 import fyersModel
from stock_sdk.logger import logger
import pandas as pd
import datetime
from stock_sdk.database.database import Session
from stock_sdk.database.models import HistoricalData, Stock
import time
from fyers_apiv3.FyersWebsocket import data_ws as ws
import pytz

class ApiCalls:
    def __init__(self):
        pass
        
    def send_login_otp(self, fy_id, app_id):
        try:
            result_string = requests.post(url=url_send_login_otp, json={"fy_id": Fy_Id, "app_id": App_Id})
            if result_string.status_code != 200:
                return [error, result_string.text]
            result = json.loads(result_string.text)
            request_key = result["request_key"]
            return [success, request_key]
        except Exception as e:
            return [error, e]


    def verify_totp(self, request_key, totp):
        try:
            result_string = requests.post(url=url_verify_TOTP, json={
                "request_key": request_key, "otp": totp})
            if result_string.status_code != 200:
                return [error, result_string.text]
            result = json.loads(result_string.text)
            request_key = result["request_key"]
            return [success, request_key]
        except Exception as e:
            return [error, e]
        
    def create_session(self):
        session = fyersModel.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_uri,
                                           response_type='code', grant_type='authorization_code')
        return session
    
    def request_otp(self):
        # Step 1 - Retrieve request_key from send_login_otp API
        send_otp_result = self.send_login_otp(fy_id=Fy_Id, app_id=App_Type)

        if send_otp_result[0] != success:
            print(f"send_login_otp failure - {send_otp_result[1]}")
            sys.exit()
        else:
            print("send_login_otp success")
        return send_otp_result[1]

    def get_access_token(self, request_key):
        # Step 2 - Verify totp and get request key from verify_otp API
        for i in range(1, 3):
            # request_key = self.send_otp_result[1]
            verify_totp_result = self.verify_totp(
                request_key=request_key, totp=pyotp.TOTP(TOPT_KEY).now())
            if verify_totp_result[0] != success:
                print(f"verify_totp_result failure - {verify_totp_result[1]}")
                time.sleep(1)
            else:
                print(f"verify_totp_result success and token created")
                break
        return verify_totp_result[1]
    
    def verify_pin_create_access_token(self, request_key_2, session):
        # Step 3 - Verify pin and send back access token
        ses = requests.Session()
        payload_pin = {"request_key": f"{request_key_2}",
                    "identity_type": "pin", "identifier": f"{pin}", "recaptcha_token": ""}
        res_pin = ses.post(
            'https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()

        ses.headers.update({
            'authorization': f"Bearer {res_pin['data']['access_token']}"
        })


        authParam = {"fyers_id": Fy_Id, "app_id": App_Id, "redirect_uri": redirect_uri, "appType": App_Type,
                    "code_challenge": "", "state": "None", "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}
        authres = ses.post('https://api.fyers.in/api/v2/token', json=authParam).json()

        url = authres['Url']

        parsed = urlparse(url)
        auth_code = parse_qs(parsed.query)['auth_code'][0]


        session.set_token(auth_code)
        response = session.generate_token()
        access_token = response["access_token"]
        print(access_token)
        return access_token

    def create_fyrs_client(self, access_token):
        fyrs_client = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path=os.getcwd())
        return fyrs_client

    def login_fyers(self):
        session = self.create_session()
        request_key = self.request_otp()
        request_key_2 = self.get_access_token(request_key)
        access_token = self.verify_pin_create_access_token(request_key_2, session)
        fyrs_client = self.create_fyrs_client(access_token)
        return fyrs_client, access_token

class FyersSocketConnection:
    def __init__(self, access_token, symbols, message_callback): 
        self.access_token = access_token
        self.symbols = symbols
        self.fyers_socket = None
        self.message_callback = message_callback

    def setup_socket(self):
        def on_message(message):
            self.message_callback(message)
            # print("Response:", message)

        def on_error(message):
            print("Error:", message)
            # Your on_error logic here

        def on_close(message):
            print("Connection closed:", message)
            # Your on_close logic here

        def on_open():
            data_type = "SymbolUpdate"
            self.fyers_socket.subscribe(symbols=self.symbols, data_type=data_type)
            self.fyers_socket.keep_running()

        self.fyers_socket = ws.FyersDataSocket(
            access_token=self.access_token,
            on_connect=on_open,
            on_close=on_close,
            on_error=on_error,
            on_message=on_message
        )
   
    def connect(self):
        self.fyers_socket.connect()

class SymbolData:
    def __init__(self, access_token):
        self.access_token = access_token
        self.session = Session()
        self.symbols = [s.symbol for s in self.session.query(Stock)]
        self.fyers_socket_connection = FyersSocketConnection(self.access_token, self.symbols, self.message_handler)
        self.market_start_time = market_start_time
        self.market_end_time = market_end_time
        self.timezone = pytz.timezone(time_zone)
      

    def create_historical_data_continuous(self):
        current_datetime = datetime.datetime.now(self.timezone)
        print("current_datetime:", current_datetime)
        market_start_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(*self.market_start_time), tzinfo=self.timezone)
        print("market_start_datetime: ", market_start_datetime)
        market_end_datetime = datetime.datetime.combine(current_datetime.date(), datetime.time(*self.market_end_time), tzinfo=self.timezone)
        print("market_end_datetime: ", market_end_datetime)
        # if market_start_datetime <= current_datetime <= market_end_datetime:
        if True:
            self.fyers_socket_connection.setup_socket()
            self.fyers_socket_connection.connect()
        else:
            print("Outside market hours")

    def message_handler(self, message):
        print("message: ", message)
        ltp = message.get('ltp')
        symbol = message.get('symbol')

        # Retrieve the stock_id based on the symbol
        stock = self.session.query(Stock).filter_by(symbol=symbol).first()
        if stock is None:
            print(f"Stock with symbol {symbol} not found in the database.")
            return

        current_datetime = datetime.datetime.now(self.timezone)  # Get the current date and time

        # Format the time to hh:mm:ss format
        formatted_time = current_datetime.strftime('%H:%M:%S')

        # Create an instance of HistoricalData and commit to the database
        historical_data = HistoricalData(
            date=current_datetime.date(),
            time=formatted_time,
            stock_id=stock.id,
            open=message.get('open_price', ltp),  # Use open_price if available, otherwise ltp
            high=message.get('high_price', ltp),  # Use high_price if available, otherwise ltp
            low=message.get('low_price', ltp),    # Use low_price if available, otherwise ltp
            close=message.get('ltp'),
            volume=message.get('vol_traded_today', 0)
        )

        # Add the historical_data instance to the session and commit
        self.session.add(historical_data)
        self.session.commit()

        print("Committed historical data:", historical_data)


# to be tested... for creating a backend of watchlist API
# import threading
# import time
# from fastapi import FastAPI, WebSocket

# app = FastAPI()

# class RealTimeDataUpdater:
#     def __init__(self, equity_data_instance, symbols):
#         self.equity_data = equity_data_instance
#         self.symbols = symbols
#         self.stop_flag = threading.Event()
#         self.update_thread = threading.Thread(target=self._update_ltp_real_time)

#     def start(self):
#         self.update_thread.start()

#     def stop(self):
#         self.stop_flag.set()
#         self.update_thread.join()

#     def _update_ltp_real_time(self):
#         self.equity_data.fs.subscribe(symbol=self.symbols)

#         while not self.stop_flag.is_set():
#             msg = self.equity_data.fs.get_message()

#             if msg:
#                 symbol = msg[0]['symbol']
#                 ltp = msg[0]['ltp']

#                 self.send_ltp_to_clients(symbol, ltp)

#     def send_ltp_to_clients(self, symbol, ltp):
#         active_connections = app.state.user_connections.get(self.symbols, set())

#         for connection in active_connections:
#             connection.send_text(f"Symbol: {symbol}, LTP: {ltp}")

# @app.websocket("/{user_id}/ws")
# async def websocket_endpoint(user_id: int, websocket: WebSocket):
#     await websocket.accept()

#     # Get or create a RealTimeDataUpdater instance for this user
#     symbols = get_symbols_for_user(user_id)
#     if symbols not in app.state.user_connections:
#         app.state.user_connections[symbols] = set()

#     app.state.user_connections[symbols].add(websocket)

#     try:
#         # Keep the WebSocket connection open until the client disconnects
#         while True:
#             data = await websocket.receive_text()
#             print(f"Received data from client: {data}")
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#     finally:
#         app.state.user_connections[symbols].remove(websocket)

# # Function to get symbols for a user (you need to implement this based on your user data)
# def get_symbols_for_user(user_id):
#     # Implement this function to fetch symbols for the user from your database or any other source
#     # For simplicity, I am returning some dummy symbols here
#     return ['NSE:HDFCBANK-EQ', 'NSE:ICICIGI-EQ', 'NSE:AUBANK-EQ']

# app.state.user_connections = {}
