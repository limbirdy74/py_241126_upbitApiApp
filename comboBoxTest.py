import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/comboBox.ui")[0]

class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox_setting()
        self.comboBox.currentIndexChanged.connect(self.menu_select)

    def comboBox_setting(self):
        dayList = ["월요일", "화요일", "수요일", "목요일", "금요일"]
        self.comboBox.addItems(dayList)

    def menu_select(self):
        comboText = self.comboBox.currentText()

        self.label.setText(comboText)



app = QApplication(sys.argv)
win = MainWindow()  # 이렇게 하면 화면에 나타났다가 사라짐. 아래를 해주면 나타났다가 엑스를 누를 때 까지 실행 됨
win.show()  # 이 문장의 위치가 손으로 만든 것 하고 차이.
sys.exit(app.exec_())
