#!/bin/env python
# -*- coding:utf-8 -*-
import os,sys,time
import traceback
import MySQLdb as mdb

import logging

"""
version: liluocheng improved at 2017-1-13, 增加来显统计功能
"""

logfilename = "Statistic." +"AT" +time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+".log"
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d %b %Y %H:%M:%S',
                        filename=logfilename,
                                        filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
#console.setLevel(logging.INFO)
console.setLevel(logging.DEBUG)
#console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')


last_day_list = [0,31,28,31,30,31,30,31,31,30,31,30,31]
VAC_RATE = 0.3*1000 #3毛钱/条 彩信

class DBAccess:
    def __init__(self):
        self.conn = None
        
    def __del__( self ):
        if self.conn is not None:
            self.conn.close()
            
    def commit( self ):
        try:
            self.conn.commit()
            return True
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return False
        
    def connect( self, host='localhost', user='mvno', passwd='123456', db='RECORD', port=3306 ):
        try:
            self.conn = mdb.connect(host, user, passwd, db, port)
            self.conn.cursor().execute("set names utf8")
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return False
        return  True
        
    def QueryBill( self, sql ):
        try:
            cursor = self.conn.cursor(mdb.cursors.DictCursor)
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return None
            
    def InsertBill( self, sql ):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.close()
            return True
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return False
    
    def QueryCallDisplayBill( self, year, month):
        first_day = "%04d-%02d-01" % (year, month)
        if month == 2:
            if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                last_day = "%04d-%02d-29" % (year, month)
            else: 
                last_day = "%04d-%02d-28" % (year, month)
        else: 
            last_day = "%04d-%02d-%02d" % (year, month, last_day_list[month]) 
        #sql = '''SELECT DISTINCT chargeNum as chargenum FROM record.bm_bi_fixedfee as fix WHERE fix.dealTime <= '%s 23:59:59' and fix.dealTime > '%s' and fix.productCode in ('PV.CND.0.1','PV.CND.0.2','PV.CND.0.3') ''' % (last_day, first_day);
        sql = '''select DISTINCT chargeNum as chargenum from record.bm_bi_fixedfee where billcycle = '%s%s00' and productCode in ('PV.CND.0.1','PV.CND.0.2','PV.CND.0.3'); ''' % ( year, month )
        logging.debug(sql)
        return self.QueryBill(sql)

    def QueryCallDisplayBillFast( self, year, month):
        first_day = "%04d-%02d-01" % (year, month)
        if month == 2:
            if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                last_day = "%04d-%02d-29" % (year, month)
            else: 
                last_day = "%04d-%02d-28" % (year, month)
        else: 
            last_day = "%04d-%02d-%02d" % (year, month, last_day_list[month]) 
        sql = '''select count(0) as totalCount from record.bm_bi_fixedfee where billcycle = '%s%s00' and productCode in ('PV.CND.0.1','PV.CND.0.2','PV.CND.0.3'); ''' % ( year, month )
        logging.debug(sql)
        return self.QueryBill(sql)

    def QueryVacList2( self, year, month):
        first_day = "%04d-%02d-01" % (year, month)
        if month == 2:
            if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                last_day = "%04d-%02d-29" % (year, month)
            else: 
                last_day = "%04d-%02d-28" % (year, month)
        else: 
            last_day = "%04d-%02d-%02d" % (year, month, last_day_list[month]) 
        sql = '''SELECT chargeNum as chargenum, fee FROM record.bm_bi_vac as vac WHERE vac.startTime <= '%s 23:59:59' 
				and vac.startTime >= '%s' and vac.callType = 1  ''' % (last_day, first_day);
        print sql
        return self.QueryBill(sql)

    def QueryVacList( self, year, month):
        billcycle= "%04d%02d00" % (year, month)
        sql = '''SELECT chargeNum as chargenum, fee FROM record.bm_bi_vac as vac 
          		WHERE callType = 1 and billCycle = %s ''' % (billcycle)
        print sql
        return self.QueryBill(sql)
       
    def QueryAreaInfo( self ):
        try:
            area_map = {}
            sql = '''select PROVINCECODE,CITYCODE,NUMBERH3 from if.INT_VOP_FILENOSECT'''
            records = self.QueryBill(sql)
            if records is None:
                print "查询号段表出错！"
                return False
            for row in records:
                area_map[row["NUMBERH3"]] = [row["PROVINCECODE"],row["CITYCODE"]]
            return area_map
        except:
            traceback.print_exc()   
            return None
    def MergeVac( self, rows, area_map ):
        try:
            result = {}
            for row in rows:
                #print row, row["fee"] 
                num = row["chargenum"][0:7]
                provcode = area_map[num][0]
                citycode = area_map[num][1]
                if citycode not in result:
                    result[citycode] = {}
                sql = '''select a.regionName as city,b.regionName as prov from common.sa_db_region a left join common.sa_db_region b 
                        on a.parentID = b.regionID where a.regionID = %s''' % citycode
                rs = self.QueryBill(sql)
                if rs is None:
                    print "查询省市信息出错，省市代码%s，%s" % (provcode, citycode)
                    continue
                for r in rs:
                    prov = r["prov"]
                    city = r["city"]
                    if "count" not in result[citycode]:
                        result[citycode]["count"] = 0
                    result[citycode]["CITYCODE"] = citycode
                    result[citycode]["PROVINCECODE"] = provcode
                    result[citycode]["cityName"] = city
                    result[citycode]["provName"] = prov
                    result[citycode]["count"] = result[citycode]["count"] + 1
                    #if "fee" not in result[citycode]:
                    #    result[citycode]["fee"] = 0L
                    #result[citycode]["fee"] +=  row["fee"]
                    break
            records = []
            for k,v in result.items():
                v["fee"] = v["count"] * VAC_RATE
                records.append(v)
            return records
        except:
            traceback.print_exc()
            return None
        

            
    def MergeCallDisplay( self, rows, area_map ):
        try:
            result = {}
            for row in rows:
                num = row["chargenum"][0:7]
                provcode = area_map[num][0]
                citycode = area_map[num][1]
                if citycode not in result:
                    result[citycode] = {}
                sql = '''select a.regionName as city,b.regionName as prov from common.sa_db_region a left join common.sa_db_region b 
                        on a.parentID = b.regionID where a.regionID = %s''' % citycode
                rs = self.QueryBill(sql)
                if rs is None:
                    print "查询省市信息出错，省市代码%s，%s" % (provcode, citycode)
                    continue
                for r in rs:
                    prov = r["prov"]
                    city = r["city"]
                    if "count" not in result[citycode]:
                        result[citycode]["count"] = 0
                    result[citycode]["CITYCODE"] = citycode
                    result[citycode]["PROVINCECODE"] = provcode
                    result[citycode]["cityName"] = city
                    result[citycode]["provName"] = prov
                    result[citycode]["count"] = result[citycode]["count"] + 1
                    break
            records = []
            for k,v in result.items():
                v["fee"] = v["count"] * 5000
                records.append(v)
            return records
        except:
            traceback.print_exc()
            return None
         
def StatisticVacBill( dbaccess, rows,billCycle ):
    try:
        totalInProv={}
        totalFee = 0
        totalCount = 0
        for row in rows:
            cityName = row["cityName"]
            provName = row["provName"]
            cityCode = int(row["CITYCODE"])
            provCode = int(row["PROVINCECODE"])
            counts = row["count"]
            fee = row["fee"]
            if provCode not in totalInProv:
                totalInProv[provCode] = {}
            if "name" not in totalInProv[provCode]:
                totalInProv[provCode]["name"] = provName
            if "count" not in totalInProv[provCode]:
                totalInProv[provCode]["count"] = counts
            if "fee" not in totalInProv[provCode]:
                totalInProv[provCode]["fee"] = fee
            else:
                totalInProv[provCode]["count"] += counts
                totalInProv[provCode]["fee"] += fee
        
            #彩信的SUB_SERVICE_TYPE为3
            sql = '''insert into settle.BM_BI_SUMFEE(SUMDATE,PROV_CODE,PROVINCE,CITY_CODE,CITY,SERVICE_CATALOG,
                  SERVICE_TYPE,SUB_SERVICE_TYPE,TOTAL_USAGE,STANDARD_FEE,SETTLE_FEE,RECEIVE_FEE) values(
                  %d,%d,'%s',%d,'%s',1,'VAC',3,%d,%d,null,null)'''
            sql = sql % (billCycle,provCode,provName,cityCode,cityName,counts,fee)
            logging.info(sql)
            #dbaccess.InsertBill(sql)
        #统计各省的总量, 地市为0.
        for k,v in totalInProv.items():
            provCode = k
            provName = v["name"]
            count = v["count"]
            fee = v["fee"]
            totalCount += count
            totalFee += fee

            sql = '''insert into settle.BM_BI_SUMFEE(SUMDATE,PROV_CODE,PROVINCE,CITY_CODE,CITY,SERVICE_CATALOG,
                  SERVICE_TYPE,SUB_SERVICE_TYPE,TOTAL_USAGE,STANDARD_FEE,SETTLE_FEE,RECEIVE_FEE) values(
                  '%s','%s','%s','%s','%s',1,'VAC',3,'%s','%s',null,null)'''
            sql = sql % (billCycle,provCode,provName, '0','0',count,fee)
            logging.debug(sql)
            #dbaccess.InsertBill(sql)
   
        #dbaccess.commit()
        return (totalCount, totalFee)
    except:
        traceback.print_exc()
        return None 
       
        
def StatisticBill( dbaccess, rows,billCycle ):
    try:
        totalInProv={}
        totalFee = 0
        totalCount = 0
        for row in rows:
            cityName = row["cityName"]
            provName = row["provName"]
            cityCode = int(row["CITYCODE"])
            provCode = int(row["PROVINCECODE"])
            counts = row["count"]
            fee = row["fee"]
            if provCode not in totalInProv:
                totalInProv[provCode] = {}
            if "name" not in totalInProv[provCode]:
                totalInProv[provCode]["name"] = provName
            if "count" not in totalInProv[provCode]:
                totalInProv[provCode]["count"] = counts
            if "fee" not in totalInProv[provCode]:
                totalInProv[provCode]["fee"] = fee
            else:
                totalInProv[provCode]["count"] += counts
                totalInProv[provCode]["fee"] += fee
            sql = '''insert into settle.BM_BI_SUMFEE(SUMDATE,PROV_CODE,PROVINCE,CITY_CODE,CITY,SERVICE_CATALOG,
                  SERVICE_TYPE,SUB_SERVICE_TYPE,TOTAL_USAGE,STANDARD_FEE,SETTLE_FEE,RECEIVE_FEE) values(
                  %d,%d,'%s',%d,'%s',1,'ATTACH',6,%d,%d,null,null)'''
            sql = sql % (billCycle,provCode,provName,cityCode,cityName,counts,fee)
            logging.debug(sql)
            #dbaccess.InsertBill(sql)
        for k,v in totalInProv.items():
            provCode = k
            provName = v["name"]
            count = v["count"]
            fee = v["fee"]
            totalFee += fee
            totalCount += count

            sql = '''insert into settle.BM_BI_SUMFEE(SUMDATE,PROV_CODE,PROVINCE,CITY_CODE,CITY,SERVICE_CATALOG,
                  SERVICE_TYPE,SUB_SERVICE_TYPE,TOTAL_USAGE,STANDARD_FEE,SETTLE_FEE,RECEIVE_FEE) values(
                  '%s','%s','%s','%s','%s',1,'ATTACH',6,'%s','%s',null,null)'''
            sql = sql % (billCycle,provCode,provName, '0','0',count,fee)
            logging.info(sql)
            #dbaccess.InsertBill(sql)
    
        #dbaccess.commit()
        return (totalCount, totalFee)
    except:
        traceback.print_exc()
        return None

"""
最后插入全国总数

"""
def StatisticFinal( dbaccess, totalCount, totalFee, subServiceType, period):
    try:
        serviceType=None
        if 6 == subServiceType: 
            #来显
            serviceType = 'ATTACH'
        elif 3 == subServiceType: 
            serviceType = 'VAC' 
    
        sql = '''insert into settle.BM_BI_SUMFEE(SUMDATE,PROV_CODE,PROVINCE,CITY_CODE,CITY,SERVICE_CATALOG, SERVICE_TYPE,SUB_SERVICE_TYPE,TOTAL_USAGE,STANDARD_FEE,SETTLE_FEE,RECEIVE_FEE) values( '%s','0','全国','0','0',1,'%s','%s','%d','%.2f',null,null)'''
        sql = sql % (period, serviceType, subServiceType, totalCount,totalFee)
        logging.info(sql)
        #dbaccess.InsertBill(sql)
        #dbaccess.commit()
        return True

    except:
        traceback.print_exc()
        return False
    



'''
参数为：账期(如201512)  业务类型(vac, attac,all. all表示所有类型都一次执行)， detail - 表示来显的会按地市分解。默认只有全国总数
'''

        
if __name__ == "__main__":
    try:
        if len(sys.argv) < 1:
            logging.error("账期%s格式不对！参数为：账期(如201512)  业务类型(vac, attac,all. all表示所有类型都一次执行)" % billDate)
            sys.exit(-1)
        billDate = sys.argv[1]
        if len(billDate) != 6 or len(sys.argv) < 3:
            logging.error("账期%s格式不对！参数为：账期(如201512)  业务类型(vac, attac,all. all表示所有类型都一次执行)" % billDate)
            sys.exit(-1)
        year = int(billDate[0:4])
        month = int(billDate[4:])
        
        type = sys.argv[2]
        subType = None
        if len(sys.argv) > 3:
            subType = sys.argv[3]
        #sys.exit(0)	
        db_record = DBAccess()
        db_record.connect('127.0.0.1', 'test', '123456', 'a', 3306)
        db_other = DBAccess()
        db_other.connect('127.0.0.1', 'test', '123456', 'if', 3306)
        area_map = db_other.QueryAreaInfo()
        if area_map is None:
            sys.exit(-1)
            
        #db_other.MergeVac(year,month);
        if(type == "vac" or type == "all"):
            vacrows = db_other.QueryVacList2(year,month);
            #print vacrows
            megrows = db_record.MergeVac(vacrows, area_map)
            logging.debug(megrows)
            vacRes = StatisticVacBill(db_other, megrows, int(billDate))
            if vacRes: 
                op = StatisticFinal(db_other, vacRes[0], vacRes[1], 3, billDate)
                if(op):
                    logging.info( "统计 [VAC] 成功！" )

        if(type == "attach" or type == "all"):
            if subType == "detail":
                #print "统计 [来显] 请用fixfee_dafei.py 脚本 "
                rows = db_other.QueryCallDisplayBill(year, month)
                print "来显\t", len(rows)
                if rows is None:
                    logging.error("查询来电显示订购数目出错，请检查！")
                    sys.exit(-1)
                #sys.exit(0)
                rows = db_record.MergeCallDisplay(rows, area_map)
                if rows is None:
                    logging.error("关联号码省市信息出错！")
                    sys.exit(-1)
                attachRes = StatisticBill(db_other, rows, int(billDate))
                if attachRes: 
                    op = StatisticFinal(db_other, attachRes[0], attachRes[1], 6, billDate)
                    if op:
                        logging.info("统计 [来显] 成功！")
            else: 

                #返回一个元组
                attachRes = db_other.QueryCallDisplayBillFast(year, month)
                if attachRes:
                    totalCount = attachRes[0]['totalCount']
                    totalFee = totalCount * 5
                    op = StatisticFinal(db_other, totalCount, totalFee, 6, billDate)
                    if op:
                        logging.info("统计 [来显] 成功！")
                
    except:
        traceback.print_exc()





