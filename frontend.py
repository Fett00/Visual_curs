import sys
import json
import backend

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

import requests
import json
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Window(QWidget):

    backend_app = backend.AppBackend()


    

    def __init__(self):

        self.tableWidjet = QTableWidget()
        self.buttonOne = QPushButton("Ok")
        self.button2 = QPushButton("Ok")
        self.button3 = QPushButton("Start")
        self.textField = QLineEdit()
        self.textField2 = QLineEdit()

        #backend class
        #self.app_backend = backend

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
        horizlayout1.addWidget(self.textField)
        horizlayout1.addWidget(self.buttonOne)

        # action btn1
        self.buttonOne.clicked.connect(self.on_ip_json)  # соединение сигнала и слота (сигнал clicked и слот on_ip_json)
        # json_file = open("example.json", "r")
        ##TEMP##
        # file = self.app_backend.get_data_and_convert_to_json()

        # TableWidjet

        self.tableWidjet.setColumnCount(3)
        self.tableWidjet.setRowCount(0)

        self.tableWidjet.setHorizontalHeaderLabels(['', 'Key', 'Value'])
        #tableWidjet.setItem(0, 1, QTableWidgetItem("Text1"))
        #tableWidjet.setItem(0, 2, QTableWidgetItem("Text3"))
        #tableWidjet.setItem(1, 2, QTableWidgetItem("Text4"))
        #tableWidjet.setItem(1, 1, QTableWidgetItem("Text2"))

        #self.tableWidjet.setCellWidget(0, 0, QCheckBox(""))
        #tableWidjet.setCellWidget(1, 0, QCheckBox("Check2"))

        formLayout1.addWidget(self.tableWidjet)

        # box3
        horizlayout2.addWidget(self.textField2)
        
        horizlayout2.addWidget(self.button2)

        #button2 action
        self.button2.clicked.connect(self.on_ip_tsdb)  # соединение сигнала и слота (сигнал clicked и слот on_ip_json)

        # засовываем горизонтальный бокс 1,2  в вертикальный бокс
        verticlayout1.addLayout(horizlayout1)
        verticlayout1.addLayout(formLayout1)
        verticlayout1.addLayout(horizlayout2)
        

        # button3 action
        self.button3.clicked.connect(self.on_auto_send)  # соединение сигнала и слота (сигнал clicked и слот on_ip_json)

        verticlayout1.addWidget(self.button3)

        generalTab.setLayout(layout)

        # Set the layout on the dialog
        layout.addLayout(verticlayout1)
        layout.addLayout(horizlayout1)
        layout.addLayout(horizlayout2)

        return generalTab

    def on_ip_json(self):

        try:
            json_ip = self.textField.text()
            #tsdb_ip = input("Enter Tsdb Ip: ")
            requests.get(json_ip)
            self.backend_app.enter_json_ip(json_ip)
            #backend.enter_tsdb_ip(tsdb_ip)

            data = self.backend_app.get_data_and_convert_to_json(self.backend_app.json_ip)

            self.tableWidjet.clear()
            self.tableWidjet.setHorizontalHeaderLabels(['Key', 'Value'])
            self.tableWidjet.setColumnCount(2)
            self.tableWidjet.setRowCount(len(data))

            if data != None or data != {}:

                counter = 0

                for i in data:
                    #self.tableWidjet.setCellWidget(counter, 0, QCheckBox(""))
                    first_item = QTableWidgetItem(i)
                    first_item.data(Qt.CheckStateRole)
                    first_item.setCheckState(Qt.Unchecked)
                    self.tableWidjet.setItem(counter, 0, first_item)
                    self.tableWidjet.setItem(counter, 1, QTableWidgetItem(str(data[i])))
                    counter += 1
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("JSON IP Address is correct")
            msg.setWindowTitle("Successful")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("JSON IP Address is incorrect")
            msg.setWindowTitle("Failed")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            


    def on_ip_tsdb(self):

        try:
            tsdb_ip = self.textField.text()
            self.backend_app.enter_tsdb_ip(tsdb_ip)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("TSDB IP Address is correct")
            msg.setInformativeText("Click start to start auto send to TSDB server")
            msg.setWindowTitle("Successful")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
        
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("TSDB IP Address is incorrect")
            msg.setWindowTitle("Failed")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()

    def on_auto_send(self):

        data_key_list = []

        try:

            for i in range(self.tableWidjet.rowCount()):
                table_item: QTableWidgetItem =  self.tableWidjet.item(i, 0)
                if table_item.checkState() > 0:
                    data_key_list.append(table_item.text())
        
            self.backend_app.auto_sender(data_key_list)

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Auto Sender stopped with error")
            msg.setWindowTitle("Failed")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    window = Window()
    window.show()
    sys.exit(app.exec_())


