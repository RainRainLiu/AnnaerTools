from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon

from gui.orderDialog import Ui_Dialog


class OrderDialog(QDialog, Ui_Dialog):
    db = 0
    def __init__(self, parent):
        super( OrderDialog, self ).__init__( parent, Qt.WindowCloseButtonHint )
        self.setupUi( self )
        self.setModal( True )
        self.checkBox_Orders_Teerace_jd.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Teerace_pdd.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Teerace_tb.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Type_succe.stateChanged.connect( self.UpdateOrderTable )
        self.checkBox_Orders_Type_wait.stateChanged.connect( self.UpdateOrderTable )
        self.comboBox_Order_TimeUnit.currentIndexChanged.connect( self.UpdateOrderTable )
        self.comboBox_Order_TimeUnit.currentIndexChanged.connect( self.UpdateWithdrawDeposit )
        self.pushButton_calculate.clicked.connect(self.UpdateScaleTable)
        self.setWindowTitle( 'AnnaerTools' )
        self.setWindowIcon( QIcon( 'main.ico' ) )
    def SetDataBase(self, dataBase):
        self.db = dataBase
        self.UpdateWithdrawDeposit()
        self.UpdateOrderTable()
        self.UpdateScaleTable()

    def UpdateWithdrawDeposit(self):
        self.SetTableViewFromList( self.tableView_tixian,
                                   self.db.GetWithdrawDeposit( self.comboBox_Order_TimeUnit.currentText() ) )

    def UpdateScaleTable(self):
        terrace = ['淘宝', '京东', '拼多多']
        state = ['交易成功']
        sacle=[(self.lineEdit_bl_9.text()), (self.lineEdit_yj_1.text(), self.lineEdit_bl_1.text()), (self.lineEdit_yj_2.text(), self.lineEdit_bl_2.text()),
               (self.lineEdit_yj_3.text(), self.lineEdit_bl_3.text()), (self.lineEdit_yj_4.text(), self.lineEdit_bl_4.text()),
               (self.lineEdit_yj_5.text(), self.lineEdit_bl_5.text()), (self.lineEdit_yj_6.text(), self.lineEdit_bl_6.text()),
               (self.lineEdit_yj_7.text(), self.lineEdit_bl_7.text()), (self.lineEdit_yj_8.text(), self.lineEdit_bl_8.text())]


        self.SetTableViewFromList( self.tableView_yongjing,
                                   self.db.GetOrders( self.comboBox_Order_TimeUnit.currentText(), terrace, state ,
                                                      scale=sacle) )


    def UpdateOrderTable(self):
        terrace = []
        state = []
        if self.checkBox_Orders_Teerace_jd.isChecked():
            terrace.append( self.checkBox_Orders_Teerace_jd.text() )
        if self.checkBox_Orders_Teerace_tb.isChecked():
            terrace.append( self.checkBox_Orders_Teerace_tb.text() )
        if self.checkBox_Orders_Teerace_pdd.isChecked():
            terrace.append( self.checkBox_Orders_Teerace_pdd.text() )

        if self.checkBox_Orders_Type_succe.isChecked():
            state.append( self.checkBox_Orders_Type_succe.text() )
        if self.checkBox_Orders_Type_wait.isChecked():
            state.append( self.checkBox_Orders_Type_wait.text() )

        self.SetTableViewFromList( self.tableView_Order,
                                   self.db.GetOrders( self.comboBox_Order_TimeUnit.currentText(), terrace, state ) )

    def SetTableViewFromList(self, tableView, list):
        model = QtGui.QStandardItemModel( tableView )
        # 设置表格属性：
        # print(list)
        model.setRowCount( len( list ) )
        model.setColumnCount( len( list[0] ) )
        # 设置表头
        for i in range( len( list[0] ) ):
            model.setHeaderData( i, Qt.Horizontal, (list[0][i]) )
        tableView.setModel( model )
        list.remove( list[0] )
        if len( list ) == 0:
            return

        for i in range( len( list[0] ) ):
            model.setItem( len( list ), i, QtGui.QStandardItem( str( 0 ) ) )

        for j in range( len( list ) ):
            orders = list[j]
            for i in range( len( orders ) ):
                model.setItem( j, i, QtGui.QStandardItem( str( orders[i] ) ) )
                try:
                    # print()
                    value = float( model.data( model.index( len( list ), i ) ) ) + float( orders[i] )
                except Exception as e:
                    print( e )
                else:
                    model.setItem( len( list ), i, QtGui.QStandardItem( str( round( value, 2 ) ) ) )
        model.setItem( len( list ), 0, QtGui.QStandardItem( "合计" ) )
        tableView.setModel( model )







