from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

def application():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle("program")
    window.setGeometry(300, 250, 350, 200)

    button = QtWidgets.QPushButton(window)
    button.move(70, 150)
    button.setText("Button")
    button.setFixedWidth(200)

    lable = QtWidgets.QLineEdit(window)
    lable.setText("enter the text")
    lable.setFixedWidth(350)



    window.show()
    sys.exit(app.exec_())

    #Структура UI построчно
    # Текстовое поле + кнопка
    # Древовидное поле QTreeWidget
    # Текстовое поле + кнопка
    # Кнопка на всю ширину


if __name__ == "__main__":
    application()
