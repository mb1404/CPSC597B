import sqlite3
import cgi
import sys


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
        
        
        
    #delete column (works, but needs a lot of work for consistency and to preserve constraints)
    def deleteCol(self,dCol):
        global dbName
        global tableName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        colNames = self.getColNames()
        colNames.remove(dCol)
        
        newTableCol =  ', '.join(colNames)
        
        c.execute("CREATE TEMPORARY TABLE t1_backup(%s);" %newTableCol)
        c.execute("INSERT INTO t1_backup SELECT %s FROM %s;" %(newTableCol,tableName))
        c.execute("DROP TABLE %s;" %tableName)
        c.execute("CREATE TABLE %s(%s);" %(tableName,newTableCol))
        c.execute("INSERT INTO %s SELECT %s FROM t1_backup;" %(tableName,newTableCol))
        c.execute("DROP TABLE t1_backup;")

   
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
        return result;

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
        

        

#t1 = table('todo.db','todo')
#print t1.SQLQuery("select * from todo8;")
#print t1.SQLQuery("INSERT INTO todo VALUES (101,'hi1','test');")




    
