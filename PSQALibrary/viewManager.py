import sqlite3
import cgi
import sys
import os
import csv


class viewManager:
    #the table name
    dbName = ''
    
    #intilaize the class object with the database name and table name
    def __init__(self,databaseName):
        global dbName
        dbName = "./SQLiteDatabases/%s" %databaseName;
        #dbName = "%s" %databaseName;        
    

    #execute SQL Query
    def SQLQuery(self,q):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        try:
            c.execute(q)
            conn.commit()
        except Exception as e:
            return "Error: %s" %e
        
        if c.description:
            col_names = [cn[0] for cn in c.description]
            
            data = c.fetchall()
            
            result = [];
            result.append(col_names)
            
            for row in data:
                result.append(list(row))
            
            conn.close()
            return result
        else:
            return "done"
            
    def dropView(self,viewName):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        
        try:
            c.execute("DROP VIEW %s" %(viewName)) 
            conn.commit()
            return "done"
        except Exception as e:
            return "Error: %s" %e
            
            
    #get view names
    def getViewNames(self):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute('SELECT name FROM sqlite_master where type="view"') 
        viewNames = c.fetchall()
            
        return viewNames;
        
    #get view SQL
    def getViewSQL(self,viewName):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("select sql from sqlite_master where name='%s'" %(viewName)) 
        sqlStatment = c.fetchall()
        
        return sqlStatment[0][0];
        
        
    #update view 
    def updateViewSQL(self,viewName,sqlStat):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor() 
        
        try:
            oldSQL = self.getViewSQL(viewName)
            c.execute("DROP VIEW %s" %(viewName))
            c.execute(sqlStat)
            conn.commit()
            return "done"
        except Exception as e:
            c.execute(oldSQL)
            return "Error: %s" %e
        
    
