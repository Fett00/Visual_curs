import sys
import json
import backend

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot


class Window(QWidget):

    def __init__(self, backend: backend.AppBackend = backend.AppBackend()):

        #backend class
        self.app_backend = backend

        super().__init__()
        self.setWindowTitle("Kursach")
        self.resize(370, 350)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "General")

        layout.addWidget(tabs)

    def generalTabUI(self):
        """Create the General page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()
        horizlayout1 = QHBoxLayout()
        horizlayout2 = QHBoxLayout()
        verticlayout1 = QVBoxLayout()
        formLayout1 = QFormLayout()

        # box1
        horizlayout1.addWidget(QLineEdit())
        buttonOne = QPushButton("Get")
        horizlayout1.addWidget(buttonOne)

        # action btn1
        buttonOne.clicked.connect(self.on_click)  # соединение сигнала и слота (сигнал clicked и слот on_click)
        # json_file = open("example.json", "r")
        ##TEMP##
        # file = self.app_backend.get_data_and_convert_to_json()

        # TableWidjet

        tableWidjet = QTableWidget()
        tableWidjet.setColumnCount(3)
        tableWidjet.setRowCount(2)

        tableWidjet.setHorizontalHeaderLabels(['CheckBox', 'Text', 'Text'])
        tableWidjet.setItem(0, 1, QTableWidgetItem("Text1"))
        tableWidjet.setItem(0, 2, QTableWidgetItem("Text3"))
        tableWidjet.setItem(1, 2, QTableWidgetItem("Text4"))
        tableWidjet.setItem(1, 1, QTableWidgetItem("Text2"))

        tableWidjet.setCellWidget(0, 0, QCheckBox("Check1"))
        tableWidjet.setCellWidget(1, 0, QCheckBox("Check2"))

        formLayout1.addWidget(tableWidjet)

        # box3
        horizlayout2.addWidget(QLineEdit())
        button2 = QPushButton("Get")
        horizlayout2.addWidget(button2)

        #button2 action
        button2.clicked.connect(self.on_clicko)  # соединение сигнала и слота (сигнал clicked и слот on_click)

        # засовываем горизонтальный бокс 1,2  в вертикальный бокс
        verticlayout1.addLayout(horizlayout1)
        verticlayout1.addLayout(formLayout1)
        verticlayout1.addLayout(horizlayout2)
        button3 = QPushButton("Start")

        # button3 action
        button3.clicked.connect(self.on_clickoff)  # соединение сигнала и слота (сигнал clicked и слот on_click)

        verticlayout1.addWidget(button3)

        generalTab.setLayout(layout)

        # Set the layout on the dialog
        layout.addLayout(verticlayout1)
        layout.addLayout(horizlayout1)
        layout.addLayout(horizlayout2)

        return generalTab

    def on_click(self):
            print('Clicked!')

    def on_clicko(self):
            print('Wake up')

    def on_clickoff(self):
            print('NYAAAA')




"""
1) ПОменять виджет дерева на виджет таблицы с тремястолбцами: столбец с чекбоксом, и два текстовых
2) Добавить функию для реакции на нажатия на кнопки
ЗАПУШИТЬ!!!!!!!!НА ГИТХАБ!!!!!

"""

   # def networkTabUI(self):    вторая страничка
        # Create the Network page UI."""
    #    layout = QVBoxLayout()
        #    layout.addWidget(QCheckBox("Network Option 1"))
        #   layout.addWidget(QCheckBox("Network Option 2"))
        #   networkTab.setLayout(layout)
    #   return networkTab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

