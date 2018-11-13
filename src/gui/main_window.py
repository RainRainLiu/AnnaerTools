from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui

from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase
from src.gui.order_dialog import OrderDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    db = 0
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.actionOpen.triggered.connect( self.openFile )


    def openFile(self):
        path = QFileDialog.getOpenFileName( self, "open file dialog", "", "DataBase(*.db)" )
        if path[0] != '':
            self.db = DataBase(path[0])
            orderDlg = OrderDialog(self)
            orderDlg.SetDataBase(self.db)
            orderDlg.show()
            #self.UpdateOrderTable()
            #self.UpdateWithdrawDeposit()
            # 在类中定义一个定时器,并在构造函数中设置启动及其信号和槽
            #self.timer = QTimer( self )
            # 设置计时间隔并启动(1000ms == 1s)
            #self.timer.start( 1000 )
            # 计时结束调用timeout_slot()方法,注意不要加（）
            #self.timer.timeout.connect( self.UpdateOrderTable )
            #self.timer.timeout.connect( self.UpdateWithdrawDeposit )







