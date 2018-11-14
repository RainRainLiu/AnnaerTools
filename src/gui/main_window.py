


from gui.mainWindow import Ui_MainWindow
from src.annaer.DataBase import DataBase
from src.gui.order_dialog import OrderDialog

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib.pyplot as plt
from pylab import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from scipy import interpolate

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        #FigureCanvas.setSizePolicy(self,
        #                          QSizePolicy.Expanding,
        #                          QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_figure(self, labels, fracs, title, imgName):
        #y = [random.randint(0, 10) for i in range(10)]
        #xx = np.linspace(0, 10)
        #f = interpolate.interp1d(x, y, 'quadratic')  # 产生插值曲线的函数
        #yy = f(xx)
        self.axes.pie( x=fracs, labels=labels, autopct='%3.1f %%',
                 shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                 )
        #self.axes.plot(x, y, 'o',xx,yy)
        self.draw()

class MainWindow(QMainWindow, Ui_MainWindow):
    db = 0
    def __init__(self):
        super( MainWindow, self ).__init__()
        self.setupUi( self )
        self.setAttribute( Qt.WA_QuitOnClose )
        self.pushButton_open_db.clicked.connect( self.openFile )
        self.pushButton_order.clicked.connect(self.Orders)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        self.m = PlotCanvas(parent=self.widget, width=5, height=4)  # 实例化一个画布对象




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
            self.updateChart()

    def Orders(self):
        orderDlg = OrderDialog( self )
        orderDlg.SetDataBase( self.db )
        orderDlg.show()

    def updateChart(self):
        tb = self.db.GetOrders( '天', ['淘宝'], ['等待收货'] )[-1]
        jd = self.db.GetOrders( '天', ['京东'], ['等待收货'] )[-1]
        pdd = self.db.GetOrders( '天', ['拼多多'], ['等待收货'] )[-1]
        title = '今日利润：' + str(round(tb[6] + jd[6] + pdd[6]))
        self.m.update_figure(['淘宝','京东','拼多多'], [tb[6], jd[6], pdd[6]], title, './1.png')
        #self.buildChart(['淘宝','京东','拼多多'], [tb[6], jd[6], pdd[6]], title, './1.png')
        #self.buildChart(['淘宝','京东','拼多多'], [tb[6], jd[6], pdd[6]], title, './1.png')
        #self.label_2.setPixmap( QPixmap( QImage(image) ) )

        #self.label_2.setPixmap(QPixmap('1.png'))

    def buildChart(self, labels, fracs, title, imgName):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.axes( aspect=1 )  # set this , Figure is round, otherwise it is an ellipse
        plt.title( title)
        plt.pie( x=fracs, labels=labels, autopct='%3.1f %%',
                 shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
                 )
        plt.savefig(imgName)
