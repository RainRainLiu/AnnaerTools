
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

    # 获取列表的第一个元素0
    def takeSecond(self, elem):
        if elem[0] == '':
            return 0
        return int(elem[0])

    def ListFindFilter(self, elem, filterIndexList):
        for filter in filterIndexList:
            if elem[filter[0]] == filter[1]:    #找到要过滤的目标
                return True
        return False


    """
    list 列表源
    takeSecond 获取列表的时间元素
    sumIndexList 求和的位置列表
    number 去除重复订单编号， 单号位置
    """
    def ListSumFormTime(self, list=[], takeSecond=0, timeUnit='', sumIndexList=[], number=None):
        try:
            list.sort(key=self.takeSecond)  # 按照时间排序
        except:
            print('按照时间排序 错误')

        resultObj = [0]
        for o in sumIndexList:
            resultObj.append( 0 )
        resultObj.append( 0 )       #数量

        resultList = []
        lastNumber = 0
        for elem in list:
            t = self.GetTimeForUnit( timeUnit, takeSecond(elem) )
            if resultObj[0] != t:   #时间变化
                resultList.append(resultObj)
                resultObj=[t]
                for o in sumIndexList:
                    resultObj.append(0)

                resultObj.append( 0 )  # 数量
            for i in range(len(sumIndexList)):
                sum = resultObj[i+2] + float(elem[sumIndexList[i]])
                resultObj.pop(i+2)  #移除旧值
                resultObj.insert(i+2, round(sum, 2))  #添加新值
                sum = resultObj[1]
                if number !=None:
                    if lastNumber != elem[number]:
                        lastNumber = elem[number]
                        sum += 1
                else:
                    sum += 1
                resultObj.pop( 1 )  # 移除旧值
                resultObj.insert( 1, sum )  # 添加新值
        resultList.append(resultObj)
        return resultList


    def GetOrders(self, timeUnit='', terrace=[], state=[], noMaster=''):

        list = [('时间', '订单数量', '总佣金', '用户佣金', '推广提成', '平台抽成', '利润', '利润率')]
        orders = []
        #过滤
        for obj in self.cursor.execute( '''select * from 订单管理''' ).fetchall():
            if state.count(obj[15]) != 0 and terrace.count(obj[1]) > 0:
                var = 0
                if obj[1] == '淘宝':
                    var = float(obj[7]) * 0.1
                elem = obj + (var,)
                orders.append(elem)
        if len(orders) == 0:
            return list
        #求和
        orders = self.ListSumFormTime(orders, self.takeSecond, timeUnit, [7, 9, 11, len(orders[0]) - 1], 6)
        #整理表头

        for obj in orders:
            if obj[2] != 0:
                profit = round(obj[2] - obj[3] - obj[4] - obj[5], 2);
                list.append((obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], profit, round(profit / obj[2], 2)))
        return list


    def GetWithdrawDeposit(self, timeUnit=''):
        deposit = self.cursor.execute( '''select * from 申请提现''' ).fetchall()
        deposit = self.ListSumFormTime( deposit, self.takeSecond, timeUnit, [6])
        deposit.insert(0,('时间', '数量','金额'))
        return deposit

    def GetMembers(self):
        list = self.cursor.execute( '''select * from 会员信息''' ).fetchall()
        return list
