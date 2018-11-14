


from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase
from src.gui.order_dialog import OrderDialog

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib.pyplot as plt
from pylab import *

class MainWindow(QMainWindow, Ui_MainWindow):
    db = 0
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.pushButton_open_db.clicked.connect( self.openFile )
        self.pushButton_order.clicked.connect(self.Orders)





    def openFile(self):
        path = QFileDialog.getOpenFileName( self, "open file dialog", "", "DataBase(*.db)" )
        if path[0] != '':
            self.lineEdit_db_path.setText(path[0])
            self.db = DataBase(path[0])
            self.updateChart()
            #self.UpdateOrderTable()
            #self.UpdateWithdrawDeposit()
            # 在类中定义一个定时器,并在构造函数中设置启动及其信号和槽
            self.timer = QTimer( self )
            # 设置计时间隔并启动(1000ms == 1s)
            self.timer.start( 1000 )
            # 计时结束调用timeout_slot()方法,注意不要加（）
            self.timer.timeout.connect( self.updateChart )

    def Orders(self):
        orderDlg = OrderDialog( self )
        orderDlg.SetDataBase( self.db )
        orderDlg.show()

    def updateChart(self):

        tb = self.db.GetOrders( '天', ['淘宝'], ['等待收货'] )[-1]
        jd = self.db.GetOrders( '天', ['京东'], ['等待收货'] )[-1]
        pdd = self.db.GetOrders( '天', ['拼多多'], ['等待收货'] )[-1]


        self.label_2.setPixmap( QPixmap( '1.png' ) )

    def buildChart(self, labels, fracs, title, imgName):
        plt.axes( aspect=1 )  # set this , Figure is round, otherwise it is an ellipse
        plt.title( title)
        plt.pie( x=fracs, labels=labels, autopct='%3.1f %%',
                 shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                 )
        plt.savefig( imgName )
