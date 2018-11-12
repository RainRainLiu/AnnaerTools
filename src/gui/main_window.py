from PyQt5.QtCore import QStringListModel, QModelIndex, Qt, QItemSelectionModel, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, \
    QFileDialog, QInputDialog, QLineEdit, QMessageBox, QHeaderView
from PyQt5 import QtGui

from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase, TimeUnit
import time

class MainWindow(QMainWindow, Ui_MainWindow):
    db = 0
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.actionOpen.triggered.connect( self.openFile )
        self.checkBox_Orders_Teerace_jd.stateChanged.connect(self.UpdateOrderTable)
        self.checkBox_Orders_Teerace_pdd.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Teerace_tb.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Type_succe.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Type_wait.stateChanged.connect( self.UpdateOrderTable )
        self.comboBox_Order_TimeUnit.currentIndexChanged.connect( self.UpdateOrderTable )

    def openFile(self):
        path = QFileDialog.getOpenFileName( self, "open file dialog", "", "DataBase(*.db)" )
        self.db = DataBase(path[0])
        self.UpdateOrderTable()

    def UpdateOrderTable(self):
        terrace = []
        state = []
        if self.checkBox_Orders_Teerace_jd.isChecked():
            terrace.append(self.checkBox_Orders_Teerace_jd.text())
        if self.checkBox_Orders_Teerace_tb.isChecked():
            terrace.append(self.checkBox_Orders_Teerace_tb.text())
        if self.checkBox_Orders_Teerace_pdd.isChecked():
            terrace.append(self.checkBox_Orders_Teerace_pdd.text())

        if self.checkBox_Orders_Type_succe.isChecked():
            state.append(self.checkBox_Orders_Type_succe.text())
        if self.checkBox_Orders_Type_wait.isChecked():
            state.append(self.checkBox_Orders_Type_wait.text())


        self.SetTableViewFromList( self.tableView_Order,
                                   self.db.GetOrders( self.comboBox_Order_TimeUnit.currentText(), terrace, state ,
                                                      self.comboBox_Orders_User.currentText()) )


    def SetTableViewFromList(self, tableView, list):
        model = QtGui.QStandardItemModel(tableView)
        # 设置表格属性：
        #print(list)
        model.setRowCount( len(list) )
        model.setColumnCount( len(list[0]) )
        # 设置表头
        for i in range(len(list[0])):
            model.setHeaderData( i, Qt.Horizontal, (list[0][i]) )
        tableView.setModel( model )
        list.remove( list[0] )
        if len(list) == 0:
            return

        for i in range(len(list[0])):
            model.setItem( len(list), i, QtGui.QStandardItem(str(0)) )

        for j in range(len(list)):
            orders = list[j]
            for i in range(len(orders)):
                model.setItem( j, i, QtGui.QStandardItem(str(orders[i])))
                try:
                    #print()
                    value = float(model.data(model.index(len(list), i))) + float(orders[i])
                except Exception as e:
                    print(e)
                else:
                    model.setItem( len( list ), i, QtGui.QStandardItem( str( round(value, 2) ) ) )
        model.setItem( len( list ), 0, QtGui.QStandardItem( "合计") )
        tableView.setModel( model )

