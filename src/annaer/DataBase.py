
import sqlite3
import time
import os
import shutil

from PyQt5.QtCore import QTimer

readDB='./reading.db'
class DataBase:
    path = ''
    conn = None
    cursor=None
    def __init__(self,dataBasePath):
        self.path = dataBasePath
        if os.path.isfile( readDB ) == True:
            os.remove( readDB )
        self.mycopyfile( self.path, './reading.db' )
        self.conn = sqlite3.connect( './reading.db' )
        self.cursor = self.conn.cursor()

    def __del__(self):
        if self.conn != None:
            self.conn.close()
            del self.conn
            del self.cursor
    """
    每次读取数据前调用，否则数据不更新
    返回文件是否变化
    """
    def updateFiel(self):
        try:
            if os.path.isfile(readDB)==False or os.path.getmtime( self.path ) > os.path.getmtime( readDB ):
                if self.conn != None:
                    self.conn.close()
                    del self.conn
                    del self.cursor
                if  os.path.isfile( readDB ) == False:
                    os.remove(readDB)
                self.mycopyfile( self.path, readDB )

                self.conn = sqlite3.connect( readDB )
                self.cursor = self.conn.cursor()
                print('update')
                return True
        except Exception as e:
            print(e)
        return False



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

    def mycopyfile(self, srcfile, dstfile):
        if not os.path.isfile( srcfile ):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split( dstfile )  # 分离文件名和路径
            if not os.path.exists( fpath ):
                os.makedirs( fpath )                # 创建路径
            shutil.copyfile( srcfile, dstfile )     # 复制文件

    # 获取列表的第一个元素0
    def takeSecond(self, elem):
        if elem[0] == '':
            return 0
        return int(elem[0])

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


    def GetOrders(self, timeUnit='', terrace=[], state=[], noMaster='', scale=[]):
        #list = [('时间', '订单数量', '总佣金', '用户佣金', '推广提成', '平台抽成（税）', '利润', '利润率%')]
        list = [('时间', '订单数量', '总佣金', '垫付金额', '平台抽成（税）', '利润', '利润率%')]
        orders = []
        #过滤
        try:
            for obj in self.cursor.execute( '''select * from 订单管理''' ).fetchall():
                if state.count(obj[15]) != 0 and terrace.count(obj[1]) > 0:
                    var = 0
                    if obj[1] == '淘宝':
                        var = float(obj[7]) * 0.1 #平台抽成
                    elif obj[1] == '京东':
                        var = float( obj[7] ) * 0.015   #2W一下的税

                    elem = obj + (var,)
                    orders.append(elem)
        except Exception as e:
            print(e)
            return list
        if len(orders) == 0:
            return list

        if len(scale) > 0:
            ordersTemp = []
            for item in orders:
                for sc in scale[1:]:
                    if float(item[7]) <= float(sc[0]):
                        try:
                            userGlod = float( item[7] ) * float( sc[1] ) / 100
                            agentGlod = userGlod * float( scale[0] ) / 100
                            obj = item[:9] + (userGlod,) + (item[10],) + (agentGlod,) + item[12:]
                            ordersTemp.append( obj )
                            break
                        except Exception as e:
                            print(e)
                            ordersTemp.append( item )
                            break
                #ordersTemp.append(item)
            orders = ordersTemp
        #求和
        orders = self.ListSumFormTime(orders, self.takeSecond, timeUnit, [7, 9, 11, len(orders[0]) - 1], 6)
        #整理表头
        for obj in orders:
            if obj[2] != 0:
                profit = round(obj[2] - obj[3] - obj[4] - obj[5], 2);
                list.append((obj[0], obj[1], obj[2], round(obj[3] + obj[4], 2), obj[5], profit, round((profit / obj[2] * 100), 2)))
        return list


    def GetWithdrawDeposit(self, timeUnit=''):
        deposit = self.cursor.execute( '''select * from 申请提现''' ).fetchall()
        deposit = self.ListSumFormTime( deposit, self.takeSecond, timeUnit, [6])
        deposit.insert(0,('时间', '数量','金额'))
        return deposit

    def GetMembers(self):
        list = self.cursor.execute( '''select * from 会员信息''' ).fetchall()
        return list
