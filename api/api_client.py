from api import *
from api.endpoints import *
from config import *
from credentials import *
import requests
import json
import time
import pyotp
import os
from urllib.parse import parse_qs, urlparse
import sys
from fyers_api import fyersModel
from fyers_api import accessToken
from logger import logger
import pandas as pd
from datetime import datetime
from database.database import Session
from database.models import HistoricalData, Stock
import time

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
        session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_uri,
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
        return fyrs_client

class EquityData:
    def __init__(self, api_obj):
        self.api_obj = api_obj
        self.session = Session()

    def get_equity_data(self, symbol):
        data = {"symbols":symbol}
        response = self.api_obj.quotes(data=data)
        return response

    def create_historical_data(self, symbol, stock_id=None):
        response = self.get_equity_data(symbol)
        data = []
        stock = self.session.query(Stock).filter_by(symbol=symbol).one()
        for stock_data in response['d']:
            historical_data = HistoricalData(
                date=datetime.fromtimestamp(stock_data['v']['tt']).strftime('%Y-%m-%d'),
                time=datetime.fromtimestamp(stock_data['v']['tt']).strftime('%H:%M:%S'),
                open=stock_data['v']['open_price'],
                high=stock_data['v']['high_price'],
                low=stock_data['v']['low_price'],
                close=stock_data['v']['lp'],
                stock=stock
            )
            if stock_id is not None:
                historical_data.stock_id = stock_id
            data.append(historical_data)
            self.session.add(historical_data)
        self.session.commit()
        return data

    def create_historical_data_continuous(self, interval_sec):
        while True:
            symbols = [s.symbol for s in self.session.query(Stock)]
            for symbol in symbols:
                data = self.create_historical_data(symbol)
                logger.info(f"Inserted {len(data)} rows into the historical_data table for {symbol}")
            time.sleep(interval_sec)

    # The below method is intended to be used to fetch data from the historical_data table.
    # Example: The ML algorithms methods can fetch data from historical table for testing    
    # def get_historical_data(self, symbol):
    #     data = self.session.query(HistoricalData).filter_by(stock_id=symbol).all()
    #     return data

    def get_historical_data(self, symbol, start_time, end_time):
        data = self.session.query(HistoricalData).filter(
            HistoricalData.stock_id == symbol,
            HistoricalData.date.between(start_time, end_time)
        ).all()
        df = pd.DataFrame([d.__dict__ for d in data])
        df = df.drop('_sa_instance_state', axis=1)
        return df




    

