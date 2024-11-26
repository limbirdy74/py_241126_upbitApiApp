import requests

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time

class UpbitApi(QThread):  # 시그널 클래스

    coinDataSent = pyqtSignal(float, float)

    def run(self):

        while True:  # 무한루프

            server_url = "https://api.upbit.com"

            params = {
                "markets": "KRW-BTC"
            }

            res = requests.get(server_url + "/v1/ticker", params=params)
            # print(res.json())
            btc_info = res.json()
            # print(btc_info[0]["trade_price"])  # 비트코인 현재가격
            tradePrice = btc_info[0]["trade_price"]
            signed_change_rate = btc_info[0]["signed_change_rate"]

            self.coinDataSent.emit(tradePrice,signed_change_rate)

            time.sleep(3)  # 업비트 호출하는 딜레이 3초로 설정

class MainWindow(QMainWindow):  # slot 클래스
    def __init__(self):
        super().__init__()

        self.upbitApi = UpbitApi()
        self.upbitApi.coinDataSent.connect(self.printCoinData)

        self.upbitApi.run()

    def printCoinData(self, btcPrice, btcChangeRate):  # slot 메소드
        print(f"비트코인 현재가격은 {btcPrice}")
        print(f"비트코인 변화율은 {btcChangeRate}")

app = QApplication(sys.argv)
win = MainWindow()  # 이렇게 하면 화면에 나타났다가 사라짐. 아래를 해주면 나타났다가 엑스를 누를 때 까지 실행 됨
win.show()  # 이 문장의 위치가 손으로 만든 것 하고 차이.
sys.exit(app.exec_())