from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase
from src.gui.order_dialog import OrderDialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from src.gui.chart import *
from pylab import mpl
import time


class MainWindow(QMainWindow, Ui_MainWindow):
    db = None
    timer=None
    first=True
    orderDlg=None
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.setWindowTitle( 'AnnaerTools' )
        self.setWindowIcon( QIcon( 'main.ico' ) )

        self.pushButton_open_db.clicked.connect( self.openFile )
        self.pushButton_order.clicked.connect(self.Orders)
        mpl.rcParams['font.sans-serif'] = ['KaiTi'] #设置字体，不设置中文乱码
        self.todayUnconfirmedChar = PlotCanvas(parent=self.widget_todayUnconfirmed, width=5, height=4, dpi=100)
        #self.todayConfirmedChar = PlotCanvas( parent=self.widget_todayUnconfirmed, width=5,height=4, dpi=100 )
        #self.withdrawDepositChar = PlotCanvas( parent=self.widget_withdrawDeposit, width=5, height=4, dpi=100 )

    def openFile(self):
        path = QFileDialog.getOpenFileName( self, "open file dialog", "", "DataBase(*.db)" )
        if path[0] != '':
            self.lineEdit_db_path.setText(path[0])
            if self.db != None:
                del self.db
            self.db = DataBase(path[0])
            self.updateChart()
            if self.timer == None:
                self.timer = QTimer( self )
                self.timer.start( 1000 )
                self.timer.timeout.connect( self.updateChart )

    def Orders(self):
        if self.orderDlg == None:
            self.orderDlg = OrderDialog( self )
        self.orderDlg.SetDataBase( self.db )
        self.orderDlg.show()

    def updateChart(self):
        self.todayUnconfirmedChar.resize( self.widget_todayUnconfirmed.width(), self.widget_todayUnconfirmed.height())
        #self.withdrawDepositChar.resize(self.widget_withdrawDeposit.width(), self.widget_withdrawDeposit.height())
        if self.db.updateFiel() or self.first:#文件有变化才刷新
            self.first=False
            unconfirmed=[]
            titleList = ['淘宝', '京东', '拼多多']
            unconfirmed.append(self.db.GetOrders( '天', ['淘宝'], ['等待收货'] ))
            unconfirmed.append( self.db.GetOrders( '天', ['京东'], ['等待收货'] ) )
            unconfirmed.append( self.db.GetOrders( '天', ['拼多多'], ['等待收货'] ) )

            todayGain = []
            todayTiTle= []

            for i in range(len(unconfirmed)):
                if self.db.GetTimeForUnit( '天', time.time() ) == unconfirmed[i][-1][0]:  # 是今天
                    todayGain.append( unconfirmed[i][-1][5] )
                    todayTiTle.append( titleList[i] )

            sh = 0
            confirmed = self.db.GetOrders( '天', ['淘宝', '京东', '拼多多'], ['交易成功'] )
            if self.db.GetTimeForUnit( '天', time.time() ) == confirmed[-1][0]:  # 是今天
                sh = confirmed[-1][5]

            tx = 0
            if self.db.GetTimeForUnit( '天', time.time() ) == self.db.GetWithdrawDeposit( "天" )[-1][0]:  # 是今天
                tx = self.db.GetWithdrawDeposit( "天" )[-1][2]

            sum = 0
            for gain in todayGain:
                if gain != '利润':
                    sum += gain
            try:
                text = '预计：' + str(round(sum, 2)) + '\n收货：'+ str(round(sh, 2)) + '\n提现：'+ str(round(tx, 2))
                self.todayUnconfirmedChar.update_figure( todayTiTle, todayGain, '今日统计：'+ str(round(sum, 2)),text )
            except Exception as e:
                print(e)

