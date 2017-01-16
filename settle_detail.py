# -*- coding:utf-8 -*-
#写EXCEL 表格脚本， 分地市
import xlwt, xlrd
import os,sys,time
import traceback
import MySQLdb as mdb
import xlutils.copy as xcopy

last_day_list = [0,31,28,31,30,31,30,31,31,30,31,30,31]

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
            self.conn.rollback()
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
    
    def DeleteBill( self, sql ):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return False
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return False

    
    def QuerySumfee( self, year, month):
        sql = "SELECT SUMDATE,PROVINCE, PROV_CODE, CITY_CODE, CITY, SUB_SERVICE_TYPE, TOTAL_USAGE, STANDARD_FEE FROM `BM_BI_SUMFEE` where SUMDATE ='%s%s' and CITY_CODE <> 0 order by city_code" %(year,month);
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
            
 
def OpenFile(filename):
    bk = xlrd.open_workbook(filename)
    try:
        table = bk.sheet_by_index(0)
    except:
        print "no sheet in 0 index "
    return table
    
def ScanTable(table):
    nrows = table.nrows
    ncols = table.ncols
    city_table_rows = 29 #每个地市表格占29行
    startrow = 4
    maxstep = (nrows-4)//city_table_rows #取下限
    sub_serice_type_col = 8
    billduration_col = 11
    settle_fee_col = 12
    city_code_col = 4
    sub_serice_type_rows = [0, 1, 2, 3, 7, 8, 9, 10, 11, 17, 25, 26,12 ]
    for i in range(maxstep):
        for rows in sub_serice_type_rows:
            cellrow = startrow+i*city_table_rows+rows
            print table.cell(cellrow, city_code_col).value
            print table.cell(cellrow, sub_serice_type_col).value, table.cell(cellrow, billduration_col).value, table.cell(cellrow, settle_fee_col).value
        
    

def WriteFile(sumfeedata, template):
    rbk = xlrd.open_workbook(template)
    wbk = xcopy.copy(rbk)
	  #wsh = wbk.add_sheet(sumfee[0][SUMDATE].join(".xlsx")
    wsh = wbk.get_sheet(0)
#    wsh.set_name(str(sumfeedata[0]["SUMDATE"]).join(".xlsx"))
    
   
#    nrows = table.nrows
#    ncols = table.ncols
    city_table_rows = 29 #每个地市表格占29行
    startrow = 4
    #maxstep = (nrows-4)//city_table_rows #取下限
    sub_serice_type_col = 8
    billduration_col = 11
    settle_fee_col = 12
    city_code_col = 4
    province_code_col = 2
    sub_serice_type_rows = [0, 1, 2, 3, 7, 8, 9, 10, 11, 17, 25, 26 ]
    sub_serice_type_rows_dict = {1:0, 2:1, 3:2, 4:3, 5:18, 8:11, 9:8, 9:9, 12:12,6:17, 15:25, 16:26 } #{sub_service_type:row_in_table}
    i = 0
    citys = []
    current_city_table_row_start = 0
    for item in sumfeedata:
        if item["CITY_CODE"] not in citys:
             current_city_table_row_start = startrow+i*city_table_rows
             wsh.write(current_city_table_row_start, city_code_col, item["CITY_CODE"])
             wsh.write(current_city_table_row_start, province_code_col, item["PROV_CODE"])
             i += 1 #下一个地市 
             citys.append(item["CITY_CODE"])
             print citys
        #print table.cell(startrow, city_code_col).value

        #print item
        print item["SUB_SERVICE_TYPE"]
        sub_serv_type_row = sub_serice_type_rows_dict[item["SUB_SERVICE_TYPE"]]
        print "row:", sub_serv_type_row
        cellrow = current_city_table_row_start+sub_serv_type_row
        #wsh.write(cellrow, sub_serice_type_col, item["SUB_SERVICE_TYPE"])
        wsh.write(cellrow, billduration_col, item["TOTAL_USAGE"])
        wsh.write(cellrow, settle_fee_col, item["STANDARD_FEE"])
         
      
    
    wbk.save(str(sumfeedata[0]["SUMDATE"])+".xlsx")

if __name__ == '__main__':
#    table = OpenFile(r"hjsj_settle.xlsx");
#
    if len(sys.argv) > 2 and sys.argv[1] == "-r":
       print "read mode"
       
       table = OpenFile(sys.argv[2]);
       ScanTable(table)
       exit()
    billDate = sys.argv[1]
    if len(billDate) != 6:
        print "账期%s格式不对！" % billDate
        sys.exit(-1)
    year = int(billDate[0:4])
    month = int(billDate[4:])

    db_record = DBAccess()
    db_record.connect('172.17.0.42', 'root', '123456', 'RECORD', 3306)
   # db_other = DBAccess()
   # db_other.connect('172.17.0.42', 'root', '123456', 'IF', 3306)

    data = db_record.QuerySumfee(year, month)
    WriteFile(data, r"hjsjtemplate.xlsx")
	#
