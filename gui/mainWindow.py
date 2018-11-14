# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(554, 418)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_db_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_db_path.setObjectName("lineEdit_db_path")
        self.gridLayout.addWidget(self.lineEdit_db_path, 0, 1, 1, 1)
        self.pushButton_open_db = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_open_db.setObjectName("pushButton_open_db")
        self.gridLayout.addWidget(self.pushButton_open_db, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.pushButton_order = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_order.setObjectName("pushButton_order")
        self.gridLayout_2.addWidget(self.pushButton_order, 0, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_open_db.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "数据库路径："))
        self.pushButton_order.setText(_translate("MainWindow", "历史订单"))

