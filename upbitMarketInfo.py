import requests
import pyupbit  # upbit 관련 모듈

url = "https://api.upbit.com/v1/market/all?is_details=true"

headers = {"accept": "application/json"}

res = requests.get(url, headers=headers)

print(res.json())

current_price = pyupbit.get_current_price("KRW-BTC")  # 해당 코인의 현재 가격
print(current_price)
ticker_list = pyupbit.get_tickers(fiat="KRW")  # 코인 종류(원화가격표시) ticker 리스트 가져오기
print(ticker_list)