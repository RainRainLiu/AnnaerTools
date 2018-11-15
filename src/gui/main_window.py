from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase
from src.gui.order_dialog import OrderDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from src.gui.chart import *
import time


class MainWindow(QMainWindow, Ui_MainWindow):
    db = 0
    timer=None
    first=True
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.pushButton_open_db.clicked.connect( self.openFile )
        self.pushButton_order.clicked.connect(self.Orders)
        mpl.rcParams['font.sans-serif'] = ['KaiTi'] #设置字体，不设置中文乱码
        #self.todayUnconfirmedChar = PlotCanvas(parent=self.widget_todayConfirmed, width=5, height=4, dpi=100)
        self.todayConfirmedChar = PlotCanvas( parent=self.widget_todayUnconfirmed, width=5,height=4, dpi=100 )
        self.withdrawDepositChar = PlotCanvas( parent=self.widget_withdrawDeposit, width=5, height=4, dpi=100 )

    def openFile(self):
        path = QFileDialog.getOpenFileName( self, "open file dialog", "", "DataBase(*.db)" )
        if path[0] != '':
            self.lineEdit_db_path.setText(path[0])
            self.db = DataBase(path[0])
            self.updateChart()
            if self.timer == None:
                self.timer = QTimer( self )
                self.timer.start( 1000 )
                self.timer.timeout.connect( self.updateChart )

    def Orders(self):
        orderDlg = OrderDialog( self )
        orderDlg.SetDataBase( self.db )
        orderDlg.show()

    def updateChart(self):
        self.todayConfirmedChar.resize( self.widget_todayUnconfirmed.width(), self.widget_todayUnconfirmed.height())
        if self.db.updateFiel() or self.first:#文件有变化才刷新
            self.first=False
            unconfirmed=[]
            confirmed = []
            titleList = ['淘宝', '京东', '拼多多']
            unconfirmed.append(self.db.GetOrders( '天', ['淘宝'], ['等待收货'] ))
            unconfirmed.append( self.db.GetOrders( '天', ['京东'], ['等待收货'] ) )
            unconfirmed.append( self.db.GetOrders( '天', ['拼多多'], ['等待收货'] ) )

            confirmed.append( self.db.GetOrders( '天', ['淘宝'], ['交易成功'] ) )
            confirmed.append( self.db.GetOrders( '天', ['京东'], ['交易成功'] ) )
            confirmed.append( self.db.GetOrders( '天', ['拼多多'], ['交易成功'] ) )
            todayGain = []
            todayTiTle= []

            for i in range(len(unconfirmed)):
                if self.db.GetTimeForUnit( '天', time.time() ) == unconfirmed[i][-1][0]:  # 是今天
                    todayGain.append( unconfirmed[i][-1][6] )
                    todayTiTle.append( titleList[i] )

            sum = 0
            for gain in todayGain:
                if gain != '利润':
                    sum += gain
            try:
                title = '今日利润：' + str(round(sum, 2))
                self.todayConfirmedChar.update_figure( todayTiTle, todayGain, title )
            except Exception as e:
                print(e)



