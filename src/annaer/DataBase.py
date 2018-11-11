
import sqlite3
import time
from enum import Enum

class TimeUnit(Enum):
    NotUse = 0
    Hour = 1
    Day = 2
    Week = 3
    Month = 4

class DataBase:
    orderList = 0
    withdrawDeposit = 0
    conn = 0
    cursor = 0
    def __init__(self,dataBasePath):
        try:
            self.conn = sqlite3.connect(dataBasePath)
            self.cursor = self.conn.cursor()
            print("Opened database successfully")
        except:
            raise
    def GetTimeForUnit(self, timeUnit='', t = 0):
        time_local = time.localtime( int(t) )
        dt = 0
        if timeUnit == '':
            dt = time.strftime( "%Y-%m-%d %H:%M:%S", time_local )
        elif timeUnit == '小时':
            dt = time.strftime( "%Y-%m-%d %H", time_local )
        elif timeUnit == '天':
            dt = time.strftime( "%Y-%m-%d", time_local )
        elif timeUnit == '周':
            dt = time.strftime( "%Y-%W", time_local )
        elif timeUnit == '月':
            dt = time.strftime( "%Y-%m", time_local )

        return dt

    # 获取列表的第一个元素
    def takeSecond(self, elem):
        if elem[0] == '':
            return 0
        return int(elem[0])

    def ListSumFormTime(self, list,timeIndex, sumIndexList, filterIndexList):

        print("")


    def GetOrders(self, timeUnit='', terrace=[], state=[], noMaster=''):
        if noMaster == '等待认领':
            orders = self.cursor.execute('''select * from 等待认领''').fetchall()
            totalIndex = 6
            userIndex = 8
            extensionIndex = 0
            stateIndex = 10
            orderIndex = 4
        else:
            orders = self.cursor.execute( '''select * from 订单管理''' ).fetchall()
            totalIndex = 7
            userIndex = 9
            extensionIndex = 11
            stateIndex = 15
            orderIndex = 5
        try:
            orders.sort(key=self.takeSecond)  # 按照时间排序
        except:
            print(orders)

        list = [('时间', '订单数量', '总佣金', '用户佣金', '推广提成', '平台抽成', '利润', '利润率' )]
        tt = 0
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0
        x5 = 0
        x6 = 0
        x7 = 0
        lastNum = 0
        for i in range(len(orders)):
            if ( terrace.count(orders[i][1]) > 0)and (state.count(orders[i][stateIndex])):
                t = self.GetTimeForUnit(timeUnit, orders[i][0])
                if tt != t:
                    if tt != 0:
                        list.append((tt, round(x1, 2), round(x2, 2), round(x3, 2), round(x4, 2), round(x5, 2), round(x6, 2), round(x7, 2)))
                        x1 = 0
                        x2 = 0
                        x3 = 0
                        x4 = 0
                        x5 = 0
                        x6 = 0
                        x7 = 0
                    tt = t
                if lastNum != orders[i][orderIndex]:
                    x1 += 1
                    lastNum = orders[i][orderIndex]

                x2 += float(orders[i][totalIndex])          #总佣金
                x3 += float(orders[i][userIndex])          #用户佣金
                x4 += float(orders[i][extensionIndex])         #推广佣金
                if orders[i][1] == '淘宝':
                    x5 += float(orders[i][7]) * 0.1 #平台抽成
                x6 = x2 - x3 - x4 - x5              #利润
                x7 = x6 / x2 * 100                  #利润率

        list.append((tt, round( x1, 2 ), round( x2, 2 ), round( x3, 2 ), round( x4, 2 ), round( x5, 2 ), round( x6, 2 )
                      ,round( x7, 2 )) )
        return list

    def GetWithdrawDeposit(self):
        list = self.cursor.execute( '''select * from 申请提现''' ).fetchall()
        return list

    def GetMembers(self):
        list = self.cursor.execute( '''select * from 会员信息''' ).fetchall()
        return list
