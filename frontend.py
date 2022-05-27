import sys
import json

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QTabWidget,
    QVBoxLayout,
    QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QTreeWidget,
)

from main import ViewTree

class ViewTree(QTreeWidget):
    def __init__(self, value):

        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QTreeWidgetItem([text])
                child.setFlags(child.flags() | Qt.ItemIsEditable)
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    new_item(item, text, val)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kursach")
        self.resize(339, 306)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "General")
    ##    tabs.addTab(self.networkTabUI(), "Network")
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
        horizlayout1.addWidget(QPushButton("Get"))

        # TreeWidjet

        json_file = open("example.json", "r")
        file = json.load(json_file)

        formLayout1.addWidget(ViewTree(file))

        # box3
        horizlayout2.addWidget(QLineEdit())
        horizlayout2.addWidget(QPushButton("Get"))

        # засовываем горизонтальный бокс 1,2  в вертикальный бокс
        verticlayout1.addLayout(horizlayout1)
        verticlayout1.addLayout(formLayout1)
        verticlayout1.addLayout(horizlayout2)
        verticlayout1.addWidget(QPushButton("Start"))



        generalTab.setLayout(layout)


        # Set the layout on the dialog
        layout.addLayout(verticlayout1)
        layout.addLayout(horizlayout1)
        layout.addLayout(horizlayout2)

        return generalTab




   # def networkTabUI(self):    вторая страничка
        """Create the Network page UI."""
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
