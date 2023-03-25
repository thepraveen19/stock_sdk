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

class api_calls:
    def __init__(self) -> None:
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

