import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Worker(QThread):  # signal 클래스

    signal1 = pyqtSignal(int, int)  # signal 메소드 -> 인수로는 슬롯으로 보내려는 값의 type

    def run(self):
        # 데이터를 만드는 작업
        self.signal1.emit(1000, 2000)

class MainWindow(QMainWindow):  # slot 클래스
    def __init__(self):
        super().__init__()

        worker = Worker()
        worker.signal1.connect(self.slot1_signal_print)

        worker.run()

    def slot1_signal_print(self, btc, eth):  # slot 메소드
        print(f"비트코인 가격은 {btc}, 이더리움 가격은 {eth}")

app = QApplication(sys.argv)
win = MainWindow()  # 이렇게 하면 화면에 나타났다가 사라짐. 아래를 해주면 나타났다가 엑스를 누를 때 까지 실행 됨
win.show()  # 이 문장의 위치가 손으로 만든 것 하고 차이.
sys.exit(app.exec_())