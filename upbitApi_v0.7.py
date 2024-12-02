## 24.12.02 upbitgAPpiTest 를 활용해서 화면에 비트코인 현재가격 보여주기.
## 24.12.02 v0.6 upbit 모듈사용. 드랍박스 추가. 코인의 종류가 변경되면 while 문을 멈추고 다시 시작하게 해야함
## 24.12.02 v0.7 코인 가격이 오을 떄 red, 내릴 떄 blue 색으로 출려되도록 변경

import requests

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pyupbit

import time

form_class = uic.loadUiType("ui/bitcoin.ui")[0]

class UpbitApi(QThread):  # 시그널 클래스

    coinDataSent = pyqtSignal(float, float)   # 시그널 함수->슬롯 함수에 데이터 전송

    def __init__(self, ticker):
    # 시그널 클래스로 객체가 선언될 떄 메인윈도우 클래스에서 ticker를 받아오도록 설계
        super().__init__()
        self.ticker = ticker
        self.alive = True  # 무한루프 종료를 위해

    def run(self):

        while self.alive:  # 무한루프

            server_url = "https://api.upbit.com"

            params = {
                "markets": self.ticker
            }

            res = requests.get(server_url + "/v1/ticker", params=params)
            # print(res.json())
            coin_info = res.json()
            # print(btc_info[0]["trade_price"])  # 코인 현재가격
            trade_price = coin_info[0]["trade_price"]
            signed_change_rate = coin_info[0]["signed_change_rate"]

            # trade_price = pyupbit.get_current_price(self.ticker)  # 입력된 코인가격 가져오기

            self.coinDataSent.emit(float(trade_price), float(signed_change_rate))  # 시그널 함수인 coinDataSent 로 가져온 코인가격

            time.sleep(3)  # 업비트 호출하는 딜레이 3초로 설정
            
    def close(self):  # 무한루프를 멈추게 함
        self.alive = False

class MainWindow(QMainWindow, form_class):  # slot 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.upbitApi = UpbitApi("KRW-BTC")  # 시그널 클래스로 객체 생성

        self.comboBox_setting()  # 콤보박스 초기화

        self.ticker_combobox.currentIndexChanged.connect(self.combobox_active)
        # 콤보박스의 메뉴를 유저가 변경하면 발생하는 이벤트 처리

        self.upbitApi.coinDataSent.connect(self.printCoinData)  # 시그널 함수와 슬롯 함수를 연결

        # self.upbitApi.run()  # Test 일 때 와는 틀리게 start() 로
        self.upbitApi.start()
        self.coinPrev = 0  # 스타일 적용을 위해. 이전 값과 비교하기 위한 초기값 설정

    def comboBox_setting(self):  # 콤보박스 초기값들 셋팅
        # 코인종류(원화가격표시) ticker 리스트 가져오기(리스트타입으로 반환)
        tickerList = pyupbit.get_tickers(fiat="KRW")
        tickerList = sorted(tickerList)  #  정렬

        # 비트코인을 제일 첫번째로
        tickerList.remove("KRW-BTC")  # 비트코인 삭제
        tickerList = ["KRW-BTC"] + tickerList  # 비트코인의 순서를 제일 첫번쨰 순서로고정

        tickerList2 = []  #  쌤은 이걸 위에 함
        for ticker in tickerList:
            tickerList2.append(ticker[4:])

        self.ticker_combobox.addItems(tickerList2)  # 콤보박스 설정

    def combobox_active(self):  # 콤보박스의 메뉴가 변경되었을 때 호출되는 함수
        selected_ticker = self.ticker_combobox.currentText()  # 현재 콤보박스에서선택된 메뉴 텍스트 가져오기
        self.ticker_label.setText(selected_ticker)
        self.upbitApi.close()  # 무한루프 종료 -> 시그널 클래스 객체가 삭제
        self.upbitApi = UpbitApi(f"KRW-{selected_ticker}")  # 시그널 클래스로 객체 생성
        self.upbitApi.coinDataSent.connect(self.printCoinData) # 시그널 함수와 슬롯 함수를 연결
        self.upbitApi.start()

    def printCoinData(self, coinPrice, signed_change_rate):  # slot 메소드
        # print(f"비트코인 현재가격은 {btcPrice}")

        self.changeRate = str(signed_change_rate)
        # if  btcPrice >= 134620000:
        #     self.alarm_label.setText("매도!!!")
        # if  btcPrice < 134620000:
        #     self.alarm_label.setText("매수!!!")

        # self.up_style()
        self.price_label.setText(f"{coinPrice:,.0f}")

        print(self.coinPrev)
        print(coinPrice)

        if self.coinPrev < int(coinPrice):
            self.price_label.setStyleSheet("color:red")
        elif self.coinPrev == int(coinPrice):
            self.price_label.setStyleSheet("color:green")
        else:
            self.price_label.setStyleSheet("color:blue")

        self.coinPrev = int(str(self.price_label.text()).replace(",",""))
    # def up_style(self):  # 변화율이 + 면 코인가격이 빨간색으로, - 면 파란색으로 표시
    #     print(self.changeRate)
    #     if "-" in self.changeRate:
    #         self.price_label.setStyleSheet("color:red")
    #     else:
    #         self.price_label.setStyleSheet("color:blue")

app = QApplication(sys.argv)
win = MainWindow()  # 이렇게 하면 화면에 나타났다가 사라짐. 아래를 해주면 나타났다가 엑스를 누를 때 까지 실행 됨
win.show()  # 이 문장의 위치가 손으로 만든 것 하고 차이.
sys.exit(app.exec_())