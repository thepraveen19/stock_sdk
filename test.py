from fyers_api.Websocket import ws
import os

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTI0NDkxMTksImV4cCI6MTY5MjQ5MTQxOSwibmJmIjoxNjkyNDQ5MTE5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazRMbGZRa3R0c3FGamhDLVB2TXU5aUdDYm5PZTVPR1pxQUd0b1U2VzE1WlFWOERRMTVzbzRkZEZLdTd0RWVGTzlEUF9pREZkcXItQmhwal9Tb0U3QVhlbXE1b080dFBDNDEzZ1ZqMWxyclRQdUZucz0iLCJkaXNwbGF5X25hbWUiOiJQUkFWRUVOIE1BTklLIEtBREFNIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZmQzNTIxNTA0MTc4YjIyMThiYjZhNmQ4ZTQ5NTYxNzBlMTdmYzdjYTBjZTgzNGUxNWI2MTQ2YjQiLCJmeV9pZCI6IlhQMjAwMzAiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.57Jg23bylJy8uMGilzZHznQkKIKdJnAa2zq3rgWcVr8"
app_id= "9X07F7VNEG-100"
access_token = f'{app_id}:{access_token}'

def custom_message(msg):
    print(989898)
    symbol = msg[0]['symbol']
    ltp = msg[0]['ltp']
    high = msg[0]['high_price']
    low = msg[0]['low_price']
    print(f"Symbol: {symbol}, LTP: {ltp}, High: {high}, Low: {low}")


def create_watchlist(access_token):
    data_type = "symbolData"
    symbols = ["NSE:HDFCBANK-EQ"]
    fs = ws.FyersSocket(access_token=access_token,run_background=False, log_path="/Users/praveenkadam/Documents/Algorithmic_trading/")
    fs.websocket_data = custom_message
    print(fs.websocket_data)
    fs.subscribe(symbol=symbols, data_type=data_type)
    fs.keep_running()

create_watchlist(access_token)


# if __name__ == '__main__':
#     main()


# msg format:
# [{'symbol': 'NSE:HDFC-EQ', 'timestamp': 1688629102, 'fyCode': 7208, 'fyFlag': 2, 'pktLen': 200, 'ltp': 2802.4, 'open_price': 2795.2, 'high_price': 2816.5, 'low_price': 2772.15, 'close_price': 2796.15, 'min_open_price': 2802.85, 'min_high_price': 2803.25, 'min_low_price': 2801.9, 'min_close_price': 2802.4, 'min_volume': 11959, 'last_traded_qty': 8, 'last_traded_time': 1688629101, 'avg_trade_price': 279207, 'vol_traded_today': 2922938, 'tot_buy_qty': 148405, 'tot_sell_qty': 147109, 'market_pic': [{'price': 2802.4, 'qty': 320, 'num_orders': 2}, {'price': 2801.7, 'qty': 327, 'num_orders': 1}, {'price': 2801.4, 'qty': 57, 'num_orders': 2}, {'price': 2801.35, 'qty': 58, 'num_orders': 3}, {'price': 2801.3, 'qty': 62, 'num_orders': 3}, {'price': 2802.45, 'qty': 186, 'num_orders': 2}, {'price': 2802.9, 'qty': 293, 'num_orders': 2}, {'price': 2802.95, 'qty': 65, 'num_orders': 2}, {'price': 2803.0, 'qty': 352, 'num_orders': 3}, {'price': 2803.1, 'qty': 96, 'num_orders': 6}]}]

###
# app_id = "9X07F7VNEG-100"

# data_type = "symbolData"
# run_background = False
# symbol = ["NSE:ONGC-EQ"]
# def custom_message(msg) :
#     print(f"Custom: {msg}")
# fyersSocket = ws.FyersSocket (access_token=ws_access_token,run_background=False, log_path= "/Users/praveenkadam/Documents/Algorithmic_trading/stock_sdk/")
# fyersSocket.websocket_data = custom_message
# fyersSocket.subscribe (symbol=["NSE:ONGC-EQ"],data_type=data_type)
# print(60)
# fyersSocket.keep_running
# print(900)


###

# def custom_message(msg):
#     print (f"Custom:{msg}") 

# def run_process_symbol_data(ws_access_token):
#     data_type = "symbolData"
#     symbol = ["NSE:SBIN-EQ"]
#     fs = ws.FyersSocket(access_token=ws_access_token,log_path= os.getcwd())
#     # fs.content = custom_message
#     fs.websocket_data = custom_message
#     fs.subscribe(symbol=symbol,data_type=data_type)
#     fs.keep_running()




# if __name__ == '__main__':
#   app_id= "9X07F7VNEG-100"
#   access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTIzMTg2ODEsImV4cCI6MTY5MjQwNTAyMSwibmJmIjoxNjkyMzE4NjgxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazNydlpXaERIQXRtYnZROUZUUVZDaFBiRDVxNXREYzV3Uy1ySU42UWVhYWp2LVhLRUJqM0puU0sxVlktLXFjMnptUGREbXVmWFNfdTN3Rkp6aTJxS1VXNWE4T1BsN3lKU1VyLXBJdTNfUldsTWQxQT0iLCJkaXNwbGF5X25hbWUiOiJQUkFWRUVOIE1BTklLIEtBREFNIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZThjNjhmNGU3NzEzNzQxNTllNzhlZTdiMTkxZTI4ODA5MWUyNDBlODE3Yjk1MzZhMjM4MWU0NzIiLCJmeV9pZCI6IlhQMjAwMzAiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.gjxQrOMYShrhsSC_gD8rgEQ7K50TgR7SxW7vmoyW9z0"
#   ws_access_token = f"{app_id}:{access_token}"
#   run_process_symbol_data(ws_access_token)

####

# def run_process_background_order_update(ws_access_token):
#     data_type = "symbolData"
#     fs = ws.FyersSocket(access_token=ws_access_token, run_background=False, log_path= os.getcwd())
#     symbol = ["NSE:SBIN-EQ"]
#     # Assign the custom_message function before subscribing
#     # print(fs.
#     fs.websocket_data = custom_message
#     fs.subscribe(data_type="symbolData", symbol=symbol)
#     fs.keep_running()

# def main():
#     app_id= "9X07F7VNEG-100"
#     access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTIzNjI0NjgsImV4cCI6MTY5MjQwNTAwOCwibmJmIjoxNjkyMzYyNDY4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazMyYmtlZXBJdExuRERJNHFQRFNuYy1YV2pXczR0YTV3LUVSeG00b2RfMVVFQS1xVk00RndjcnprT3hLVGVQZHQzQk9YWVEwTERIelB3Uzd6U3VMZkgyRWZjanRmYWlBNnR2eXhIZ0dCYk9OSEx0cz0iLCJkaXNwbGF5X25hbWUiOiJQUkFWRUVOIE1BTklLIEtBREFNIiwib21zIjoiSzEiLCJoc21fa2V5IjoiMWI2ZDg4NGM3ZmEyOGM3ZjQ5NjA1ZmJhZjllNDc3Y2RhYTkwMDZiOWVlOTIwN2U1OWJkYmI2MGYiLCJmeV9pZCI6IlhQMjAwMzAiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.3wwWJb6ixCCPw-EgtTvNvXXWkln2Tu4RkI_Th8qhB20"
#     # access_token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTIzNjA0NDEsImV4cCI6MTY5MjQwNTAyMSwibmJmIjoxNjkyMzYwNDQxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazMxNzVRdnF5cEhMeG5wRmlMMU1BVHBxeHVuMUhxb1ZRMzFYeUxBeVg0OHNXMHp2UDFVTFVRdWhnN1JVZE5HX3dFekkzSUtIb2hlUW5mVldzT2E0VlJhUTJxOHZmUXVjWlpjbXFBQTFUcEVFeG5DTT0iLCJkaXNwbGF5X25hbWUiOiJQUkFWRUVOIE1BTklLIEtBREFNIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYWFiY2E0YWFkNTVhMDFhN2YyZjIwMDliOGVjZTg4NWE5ZTZlZDc5OGRmOTkxMTIxYzRlY2U4NWMiLCJmeV9pZCI6IlhQMjAwMzAiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.Ebybqro_FCi8fVyVjGRHV8IzHYm2_B3HSQECA4wfPEE"
#     ws_access_token = f"{app_id}:{access_token}"
#     # access_token = "L9*****BW-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9******************************lcnMuaW4iLCJpYXQiOjE2MzE1ODY2MzUsImV4cCI6MTYzMTY2NTgzNSwibmJmIjoxNjMxNTg2NjM1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaFFBbExjOTlIUG85TTF4LWl5bTBZRFRHMHhXSi1HVGRkNU5BWlFET2xXYUpIS2h4S2RjMXVYckthc1R3VGlDQ01sYTBhanp6SmYwSWtHSHVFQjcwTThUcFcxckctQUdOWGZlQWhzZVY0bTVRSm1FRT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.Dacrm4oZU1Vcarr3nW8rKueJpVNBJCNVvdjg0cDMQrQ"
#     run_process_background_order_update(ws_access_token)

# if __name__ == '__main__':
#     main()
