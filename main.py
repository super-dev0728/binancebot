import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

import client
import global_var
import price
import wallet
from threading import Thread, Event

event = Event()
t2 = Thread(target=price.generateCandle, args=(event, ))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.mainLayout = QGridLayout()
        self.createToolbar()
        self.mainLayout.addWidget(self.tableWidget, 1, 0, 1, 12)
        self.createStatus()
        self.createManualCtrl()
        self.setLayout(self.mainLayout) 

        self.resize(800, 600)
        self.setWindowTitle("Binance BTCUSDT")
        # Show widget
        self.show()
    
    def createToolbar(self):
        scanBtn = QPushButton("S&etting")
        scanBtn.setFixedHeight(32)
        scanBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        scanBtn.clicked.connect(lambda: self.setting())
        self.mainLayout.addWidget(scanBtn, 0, 10, 1, 1)

        scanBtn = QPushButton("&Wallet")
        scanBtn.setFixedHeight(32)
        scanBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        scanBtn.clicked.connect(lambda: self.viewwallet())
        self.mainLayout.addWidget(scanBtn, 0, 11, 1, 1)
    
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setFont(QFont('Arial', 14))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Time", "Open", "High", "Low", "Close", "Volume"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
    
    def createStatus(self):
        self.priceLabel = QLabel("")
        self.priceLabel.setStyleSheet("font-size: 32px;")
        self.chgLabel = QLabel("")
        self.mainLayout.addWidget(self.priceLabel, 2, 2, 1, 3)
        self.mainLayout.addWidget(self.chgLabel, 2, 7, 1, 2)
    
    def createManualCtrl(self):
        buyGroup = QGroupBox("BUY BTC")
        buyGroup.setStyleSheet("color: #000; font-weight: bold; font-size: 20px;")
        buyLayout = QVBoxLayout()
        buyEditLayout = QHBoxLayout()
        buyLabel = QLabel("Amount:")
        buyLabel.setStyleSheet("font-size: 16px;")
        self.buyEdit = QLineEdit('')
        self.buyEdit.setFixedHeight(32)
        self.buyEdit.setStyleSheet("font-size: 18px;")
        buyBtn = QPushButton("&BUY")
        buyBtn.setFixedHeight(32)
        buyBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_blue))
        buyBtn.clicked.connect(lambda: self.buy())
        buyEditLayout.addWidget(buyLabel)
        buyEditLayout.addWidget(self.buyEdit)
        buyLayout.addLayout(buyEditLayout)
        buyLayout.addWidget(buyBtn)
        buyGroup.setLayout(buyLayout)
        self.mainLayout.addWidget(buyGroup, 3, 1, 1, 4)

        sellGroup = QGroupBox("SELL BTC")
        sellGroup.setStyleSheet("color: #000; font-weight: bold; font-size: 20px;")
        sellLayout = QVBoxLayout()
        sellEditLayout = QHBoxLayout()
        sellLabel = QLabel("Amount:")
        sellLabel.setStyleSheet("font-size: 16px;")
        self.sellEdit = QLineEdit('')
        self.sellEdit.setFixedHeight(32)
        self.sellEdit.setStyleSheet("font-size: 18px;")
        sellBtn = QPushButton("&SELL")
        sellBtn.setFixedHeight(32)
        sellBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color=global_var.color_red))
        sellBtn.clicked.connect(lambda: self.sell())
        sellEditLayout.addWidget(sellLabel)
        sellEditLayout.addWidget(self.sellEdit)
        sellLayout.addLayout(sellEditLayout)
        sellLayout.addWidget(sellBtn)
        sellGroup.setLayout(sellLayout)
        self.mainLayout.addWidget(sellGroup, 3, 7, 1, 4)
    
    def setStatus(self, price, chg):
        price = float(price)
        price = round(price, 2)
        chg = float(chg)
        chg = round(chg, 5)
        if chg < 0:
            self.chgLabel.setStyleSheet("font-size: 24px;font-weight:bold;color:{color}".format(color=global_var.color_red))
        else:
            self.chgLabel.setStyleSheet("font-size: 24px;font-weight:bold;color:{color}".format(color=global_var.color_blue))
        self.priceLabel.setText(str(price))
        self.chgLabel.setText(str(chg)+'%')
    
    def addRow(self, data):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(data['time']))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(data['o']))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(data['h']))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(data['l']))
        self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(data['c']))
        self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(data['v']))

    def viewwallet(self):
        self.tmp_w = wallet.App(client.getWallet())
        self.tmp_w.show()
        pass

    def setting(self):
        pass
    
    def buy(self):
        try:
            val = float(self.buyEdit.text())
            client.buymarket('BTCUSDT', val)
        except ValueError:
            pass

    def sell(self):
        try:
            val = float(self.sellEdit.text())
            client.sellmarket('BTCUSDT', val)
        except ValueError:
            pass

    def closeEvent(self, evt):
        print('-------------exit---------')
        event.set()
        os._exit(1)

if __name__ == '__main__':
    client.init()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qp = QPalette()
    qp.setColor(QPalette.ButtonText, QColor(20, 20, 20))
    qp.setColor(QPalette.WindowText, Qt.black)
    qp.setColor(QPalette.Window, QColor(150, 210, 250))
    qp.setColor(QPalette.Button, Qt.gray)
    app.setPalette(qp)

    t2.start()

    global_var.gmain_dlg = App()
    sys.exit(app.exec_())
