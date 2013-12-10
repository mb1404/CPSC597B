import sqlite3
import cgi
import sys
import os
import csv


class table:
    #the table name
    dbName = ''
    tableName = ''
    
    #intilaize the class object with the database name and table name
    def __init__(self,databaseName,table_Name):
        global dbName
        global tableName
        dbName = "./SQLiteDatabases/%s" %databaseName;
        #dbName = "%s" %databaseName;
        tableName = table_Name
        
    
    #add column
    def addColumn(self,colName,colType,isNull,defaultVal):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        q="ALTER TABLE %s ADD COLUMN %s %s " %(tableName,colName,colType)
        
        if isNull == "True":
            q = q + "NOT NULL "
        if defaultVal:
            q = q + "Default %s " %defaultVal
        
        try:
            c.execute(q) 
            return "Succesfull"
        except Exception as e:
            return "Error: %s" %e
        
        
        
    #delete column
    def deleteCol(self,dCol):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        colNames = self.getColNames()
        colNames.remove(dCol)
        
        if len(colNames) == 0 :
            return "Error: Zero-column tables aren't supported in SQLite"

        
        newTableCol =  ', '.join(colNames)
        c.execute("CREATE TEMPORARY TABLE t1_backup(%s);" %newTableCol)
        c.execute("INSERT INTO t1_backup SELECT %s FROM %s;" %(newTableCol,tableName))
        
        c.execute('select sql from sqlite_master where type = "table" and name="%s" and tbl_name = "%s"' %(tableName,tableName) )
        result = c.fetchall()
        oldSQLstat = result[0][0]
        sqlpart1 = oldSQLstat[ 0 : oldSQLstat.index("(") ]
        sqlpart2 = oldSQLstat[ oldSQLstat.index("(")+1 : oldSQLstat.index(")") ]
        colDefList = sqlpart2.split(",")
        for colDef in colDefList:
            if dCol in colDef:
                colDefList.remove(colDef)
        newSQLstat = sqlpart1 + "( " +  ",".join(colDefList) + ")"

        c.execute("DROP TABLE %s;" %tableName)
        c.execute(newSQLstat)
        c.execute("INSERT INTO %s SELECT %s FROM t1_backup;" %(tableName,newTableCol))
        c.execute("DROP TABLE t1_backup;")
        return "Succesfull"

   
    #get column names
    def getColNames(self):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("PRAGMA table_info(%s)" %(tableName)) 
        result = c.fetchall()

        colNamesList = []
        for r in result:
            colNamesList.append(r[1])
            
        return colNamesList
    
   

    
    #get one column Info
    #the returned value will be a list in the following format:
    # [cid,name,type,notnull,dflt_value,pk]
    # e.g. [1,task,char(100),1,None,0 ]
    def getColInfo(self,colName):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("PRAGMA table_info(%s)" %(tableName)) 
        result = c.fetchall()

        for r in result:
            if r[1] == colName:
                return r
                
    #get all columns Info
    #the returned value will be a list of list in the following format:
    # [cid,name,type,notnull,dflt_value,pk]
    # e.g. [[1,task,char(100),1,None,0 ],[1,name,char(100),1,None,0 ]]
    def getAllColsInfo(self):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("PRAGMA table_info(%s)" %(tableName)) 
        result = c.fetchall()
        
        tColInfo = []
        
        for row in result:
            row = list(row)
            if row[3] == 0:
                row[3] = "Null"
            else:
                row[3] = "Not Null"
                
            if row[5] == 0:
                row[5] = "No"
            else:
                row[5] = "Yes"
            
            tColInfo.append(row)
                
        
        return tColInfo;
        

    #insert a raw
    #the row data provided are in a list
    def insertRow(self,rowData):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        values = str(rowData)
        values = values.replace("[",'',1)
        values = values.replace("]",'',1)
        try:
            c.execute("INSERT INTO %s VALUES (%s);" %(tableName,values)) 
            conn.commit()
            #print "INSERT INTO %s VALUES (%s);" %(tableName,values)
            conn.close()
            return "Succesfull"
        except Exception as e:
            return "Error: %s" %e
            
    #update row
    #the row data provided are in a list of list [[col1,data],[col2,data],[col3,data]...]
    def updateRow(self,rowData,rowID):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        values = str(rowData)
        values = values.replace("[",'',1)
        values = values.replace("]",'',1)
        
        SQLStat = "UPDATE %s SET " %(tableName)
        
        for col in rowData:
            SQLStat = SQLStat + "%s = '%s' , " %(col[0],col[1])
        
        SQLStat = SQLStat + " WHERE rowid = '%s'" %(rowID)
        
        li = SQLStat.rsplit(",",1)
        SQLStat = "".join(li)

        try:
            c.execute(SQLStat) 
            conn.commit()
            #print "INSERT INTO %s VALUES (%s);" %(tableName,values)
            conn.close()
            return "Succesfull"
        except Exception as e:
            return "Error: %s" %e
            
    
    
    #delete a raw based in rowid
    def deleteRow(self,rowid):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("delete from %s where rowid = %d;" %(tableName,rowid)) 
        conn.commit()
        conn.close()
        
    #get data
    #the data will be represented as list of tuples
    def getData(self):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        c.execute("select *,rowid from %s" %(tableName))
        data = c.fetchall()
        conn.close()
        return data
        
        
    #get one Row data including col names
    #the data will be represented as list of lists e.g " [["bookID","100"],["title","Java"],["price","$25"]]     "
    def getRowData(self,rowid):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        colNames = self.getColNames()
        colNamesStr = ",".join(colNames)
        
        c.execute("select %s from %s where rowid = %s" %(colNamesStr,tableName,rowid))
        data = c.fetchall()
        data = list(data[0])
        conn.close()
        
        rowData = []
        index = 0
        for colN in colNames:
            rowData.append([colN,data[index]])
            index = index + 1
            
        return rowData
        
    def generateCSVFile(self):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        colNames = self.getColNames()
        
        c.execute("select * from %s" %(tableName))
        data = c.fetchall()
        data.insert(0,colNames)
        
        with open("./temp/exportFiles/%s.csv" %(tableName), 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(data)
      
        conn.close()
        
    def importCSV(self,cvsfile):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        message = ""
        #check the csv file is correct and match the table columns
        colNames = self.getColNames()
        
        with open(cvsfile, 'rb') as f:
            reader = csv.reader(f)
            reader = list(reader)
            csvFileColNames = reader.pop(0)
            
            if colNames != csvFileColNames:
                return "The CSV file is invalid"
        
        #insert the data, return an error message if an exception is raised
        norows = len(reader)
        for row in reader:
            insertMessage = self.insertRow(row)
            if "Error" in insertMessage:
                return insertMessage
        #send sucess message
        return "%d rows were imported successfully" %(norows)
        

#t1 = table('Chinook2.db','Customer')
#print t1.getAllIndicesInfo()

        
        
#t1 = table('Library.db','Book')
#print t1.importCSV("Book.csv")
#t1.GenerateCSVFile()


#t1 = table('todo.db','todo')
#print t1.SQLQuery("select * from todo8;")
#print t1.SQLQuery("INSERT INTO todo VALUES (101,'hi1','test');")




    
