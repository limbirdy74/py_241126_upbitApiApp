import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pyupbit

import time

form_class = uic.loadUiType("ui/bitcoin.ui")[0]  # 외부 ui 불러오기


class UpbitApi(QThread):  # 시그널 클래스->스레드 클래스

    coinDataSent = pyqtSignal(float)  # 시그널 함수->슬롯 함수에 데이터 전송

    def __init__(self, ticker):
        # 시그널 클래스로 객체가 선언될 때 메인윈도우 클래스에서 ticker를 받아오도록 설계
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:  # 무한루프(3초에 한번씩 실행)
            # server_url = "https://api.upbit.com"
            # params = {
            #     "markets": "KRW-BTC"
            # }
            # res = requests.get(server_url + "/v1/ticker", params=params)
            # # print(res.json())
            # btc_info = res.json()
            # # print(btc_info[0]["trade_price"])  # 비트코인의 현재가격
            # trade_price = btc_info[0]["trade_price"]  # 비트코인의 현재가격
            # signed_change_rate = btc_info[0]["signed_change_rate"]  # 비트코인의 가격 변화율

            trade_price = pyupbit.get_current_price(self.ticker)  # 입력된 코인의 가격 가져오기
            print(trade_price)
            self.coinDataSent.emit(float(trade_price))  # 시그널 함수인 coinDataSent로 가져온 코인가격 데이터를 제출

            time.sleep(3)  # 업비트 호출하는 딜레이 3초로 설정

    def close(self):
        self.alive = False


class MainWindow(QMainWindow, form_class):  # 슬롯 클래스
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.upbitapi = UpbitApi("KRW-BTC")  # 시그널 클래스로 객체 생성

        self.comboBox_setting()  # 콤보박스 초기화 메소드 호출
        self.ticker_combobox.currentIndexChanged.connect(self.comboBox_active)
        # 콤보박스의 메뉴를 유저가 변경하면 발생하는 이벤트 처리
        self.upbitapi.coinDataSent.connect(self.printCoinData)  # 시그널 함수와 슬롯 함수를 연결
        self.upbitapi.start()
        # self.upbitapi.run()

    def comboBox_setting(self):  # 콤보박스 초기값들 셋팅
        # 코인 종류(원화가격표시) ticker 리스트 가져오기(리스트 타입으로 반환)
        tickerList = pyupbit.get_tickers(fiat="KRW")

        tickerList2 = []
        for ticker in tickerList:
            tickerList2.append(ticker[4:])  # KRW- 제거

        tickerList2 = sorted(tickerList2)
        tickerList2.remove("BTC")  # 비트코인 ticker 삭제
        tickerList2 = ["BTC"] + tickerList2  # 비트코인 ticker를 제일 첫번째 순서로 고정
        self.ticker_combobox.addItems(tickerList2)  # 콤보박스 셋팅

    def comboBox_active(self):  # 콤보박스의 메뉴가 변경되었을 때 호출되는 메소드
        selected_ticker = self.ticker_combobox.currentText()  # 현재 콤보박스에서 선택된 메뉴 텍스트 가져오기
        self.ticker_label.setText(selected_ticker)
        self.upbitapi.close()  # 시그널 클래스의 while문 무한루프가 정지->시그널 클래스 객체가 삭제
        self.upbitapi = UpbitApi(f"KRW-{selected_ticker}")  # 시그널 클래스로 새로운 객체 생성
        self.upbitapi.coinDataSent.connect(self.printCoinData)  # 시그널 함수와 슬롯 함수를 연결
        self.upbitapi.start()

    def printCoinData(self, coinPrice):  # 슬롯 함수->시그널 함수에서 보내준 데이터를 받아주는 함수
        print(f"비트코인의 현재가격: {coinPrice}")

        # if btcPrice >= 134673000:
        #     self.alarm_label.setText("매도!!!");
        # if btcPrice <= 134660000:
        #     self.alarm_label.setText("매수!!!");

        self.price_label.setText(f"{coinPrice:,.0f}")


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())