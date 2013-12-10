import sqlite3
import cgi


class database1:
    #the database name
    dbName = ''
    
    #intilaize the class object with the database name
    def __init__(self,databaseName):
        global dbName
        dbName = "./SQLiteDatabases/%s" %databaseName
        #dbName = "%s" %databaseName;
        
        
    # create a table
    # the table must have at least one column with its type
    # other columns are optional and must be provided as a list of lists
    #each inside list should be in the following format
    #[col Name, col Type, not null,default value,is auto incriment,is pk]
    # primary key (true or false), not null(true of false), auto increment(true or false),default value  (none,default value)  
    #e.g. ['price',smallint,True,None,False,False]
    def createTable(self,tableName,colList = None):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        q = "create table %s (" %(tableName)
        
        """if tableName in self.getTablesNames():
            return "Error, The table already exists";"""
    
        if colList:
            for col in colList:
                if (col[1] != "INTEGER") and (col[4] == "True"):
                    return "Error, AUTOINCREMENT is only allowed on an INTEGER PRIMARY KEY";
                
                if (col[1] == "INTEGER") and (col[4] == "True") and (col[5] == "False"):
                    return "Error, AUTOINCREMENT is only allowed on an INTEGER PRIMARY KEY";
                
                q = q + "%s %s " %(col[0],col[1])  #col name and type
                if col[5] == "True":  #if primary key
                    q = q + "PRIMARY KEY "
                    if col[4] == "True": #if auto increment
                        q = q + "AUTOINCREMENT "
                if col[2] == "True":  #if col is not null
                    q = q + "NOT NULL "
                if col[3]: #if default value is set
                    q = q + "Default %s " %(str(col[3]))
                    
                q = q + ","
                
            q = q + ");"
            
        else:
             q = q + ");"
        
        q = q.replace(",);",");")
        try:
            c.execute(q) 
            return "The Table was created succesfully"
        except Exception as e:
            return "Error: %s" %e
        
    #drop a table
    def dropTable(self,tableName):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        q = "drop table if exists %s;" %(tableName);
        
        try:
            c.execute(q) 
            return "The Table was dropped succesfully"
        except Exception as e:
            return "Error: %s" %e

        
    # return a list of the database table names 
    def getTablesNames(self):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' and name != 'sqlite_sequence' order by name;")
        result = c.fetchall()
        tablesNamesList = []
        for r in result:
            tablesNamesList.append(r[0])
            
        return tablesNamesList
        
    # is valid sqlite database
    def isValidSQliteDatase(self):
        global dbName
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        try:
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return True
        except Exception as e:
            return False
        
        return tablesNamesList
     
    #check if a table exist in the database
    def doesTableExist(self,tableName):
        AllTableNames = self.getTablesNames()
        if tableName in AllTableNames:
            return True
        else:
            return False
        
        
    #execute SQL Query
    def SQLQuery(self,q):
        global dbName
        global tableName
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

#t1 = database('todo.db')

"""tn = "tb1"
cols = [['id','INTEGER',False,None,True,True],
['Name','varchar(10)',True,None,False,False],
['age','varchar(10)',False,'18',False,False]]

t1.createTable(tn,cols)"""
#print t1.getTablesNames()

#t1 = database1('todo.db')
#print t1.SQLQuery("select * from todo;")
#print t1.SQLQuery("INSERT INTO todo VALUES (102,'hi2','test');")

























    
