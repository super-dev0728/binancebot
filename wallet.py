from PyQt5.QtWidgets import (QWidget, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout)
from PyQt5.QtGui import QFont

class App(QWidget):
    def __init__(self, data):
        super().__init__()
        self.initUI(data)
        
    def initUI(self, data):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable(data)

        # Add box layout, add table to box layout and add box layout to widget
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.tableWidget, 1, 0, 1, 12)
        self.setLayout(self.mainLayout) 

        self.resize(400, 400)
        self.setWindowTitle("Binance Wallet")
        # Show widget
        self.show()
    
    def createTable(self, data):
        self.tableWidget = QTableWidget()
        self.tableWidget.setFont(QFont('Arial', 14))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Asset", "Free", "Lock"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        for x in data:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(x['asset']))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(x['free'])))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(x['locked'])))

    def closeEvent(self, evt):
        self.hide()
