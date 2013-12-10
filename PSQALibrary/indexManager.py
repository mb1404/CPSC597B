import sqlite3
import cgi
import sys
import os
import csv


class indexManager:
    #the table name
    dbName = ''
    
    #intilaize the class object with the database name and table name
    def __init__(self,databaseName):
        global dbName
        dbName = "./SQLiteDatabases/%s" %databaseName;
        #dbName = "%s" %databaseName;        
    

    #create and index, the columns names should be provided as a list
    def createIndex(self,indexName,tableName, colNames):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        colNameStr =   ', '.join(colNames)
        #print "CREATE INDEX %s on %s (%s)" %(indexName,tableName,colNameStr)
        
        try:
            c.execute("CREATE INDEX %s on %s (%s)" %(indexName,tableName,colNameStr)) 
            conn.commit()
            conn.close()
            return "The index was created succesfully"
        except Exception as e:
            return "Error: %s" %e

    #drop an index
    def dropIndex(self,indexName):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
    
        try:
            c.execute("DROP INDEX %s" %(indexName)) 
            conn.commit()
            conn.close()
            return "Succesfull"
        except Exception as e:
            return "Error: %s" %e
            
    #get all user-created indices whith thier info, represented as list of list
    #each index will be represented as list with formate [name,table]
    def getAllIndicesInfo(self):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute('SELECT name,tbl_name FROM sqlite_master where type="index" and name not like "IPK_%" and name not like "IFK_%" and name not like "sqlite_autoindex_%"') 
        indices1 = c.fetchall()
        indCols = []
        result = []
        
        for ind in indices1:
            indInfo = c.execute('PRAGMA index_info(%s)' %(ind[0])) 
            indCols = []
            for row in indInfo:
                indCols.append(row[2])
            result.append([ind[0],ind[1],indCols])
            
            
        return result;





    
