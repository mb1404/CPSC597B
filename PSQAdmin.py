import sqlite3
from bottle import route, run, debug, template, request, validate, static_file, error,redirect
from bottle import default_app
from PSQALibrary.databaseManager import * 
from PSQALibrary.database1 import * 
from PSQALibrary.table import * 


#index page
@route('/')
def index():
    dbmanager = databaseManager();
    dbNames = dbmanager.getDatabaseNames();
    output = template('./templates/index/index',dbNames=dbNames)
    return output;
    
#index page with database chosen
@route('/database/:choosenDB')
def database(choosenDB):
    dbmanager = databaseManager();
    dbNames = dbmanager.getDatabaseNames();
    t1 = database1(choosenDB)
    tablesList = t1.getTablesNames();
    output = template('./templates/index/database',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
    return output;
    
#create database page
@route('/createdb')
def createdb():
    #get database name and create the database
    if request.GET.get('create_db_btn','').strip():
        newDBName = request.GET.get('databaseName','').strip()
        message=""
        dbmanager = databaseManager();
        
        if dbmanager.doesDBExists(newDBName):
            dbNames = dbmanager.getDatabaseNames();
            message="The Database already exists"
            output = template('./templates/createDatabase/createdbconf',dbNames=dbNames,message=message)
            return output;
        
        else:
            dbmanager.createDatabase(newDBName)
            message="The database was created succesfully"
            dbNames = dbmanager.getDatabaseNames();
            output = template('./templates/createDatabase/createdbconf',dbNames=dbNames,message=message)
            return output;
            
    #show the form
    else:
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        output = template('./templates/createDatabase/createdb',dbNames=dbNames)
        return output;
        
        
#Drop database page
@route('/dropdb')
def dropdb():
    #get database name and drop the database
    if request.GET.get('drop_db_btn','').strip():
        d_DBName = request.GET.get('databaseName','').strip()
        message=""
        dbmanager = databaseManager();

        dbmanager.dropDatabase(d_DBName)
        message="The database was dropped succesfully"
        dbNames = dbmanager.getDatabaseNames();
        output = template('./templates/DropDatabase/dropdbconf.tpl',dbNames=dbNames,message=message)
        return output;
            
    #show the form
    else:
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        output = template('./templates/DropDatabase/dropdb',dbNames=dbNames)
        return output;
    
    
#Create a table
@route('/database/:choosenDB/createTable')
def createTable(choosenDB):
    
    if request.GET.get('create_table_btn','').strip():
        
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        
        message=""
        
        index = 1;
        AllCols = [];
        while(True):
            if request.GET.get('ColName%s' %index,'').strip():
                columnAtr = []
                columnAtr.append(request.GET.get('ColName%s' %index,'').strip());
                columnAtr.append(request.GET.get('colType%s' %index,'').strip());
                columnAtr.append(request.GET.get('isNull%s' %index,'').strip());
                columnAtr.append(request.GET.get('defaultValue%s' %index,'').strip());
                columnAtr.append(request.GET.get('isAI%s' %index,'').strip());
                columnAtr.append(request.GET.get('isPK%s' %index,'').strip());
                index = index + 1;
                AllCols.append(columnAtr);
            
            else:
                break;
        
        t1 = database1(choosenDB)
        message = t1.createTable(request.GET.get('tableName','').strip(),AllCols)
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        
        output = template('./templates/createTable/createtableconf',dbNames=dbNames,message=message,choosenDB=choosenDB,tablesList=tablesList)
        return output;
        
    else:
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        output = template('./templates/createTable/createtable',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
        return output;
    
    
#Drop a table
@route('/database/:choosenDB/dropTable')
def dropTable(choosenDB):

    if request.GET.get('drop_table_btn','').strip():
        
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        
        message=""
        
        tableName = request.GET.get('tableName','').strip();
        if tableName:
              t1 = database1(choosenDB)
              message = t1.dropTable(tableName);
        else:
            message = "Error, no table was chosen"
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
    
        output = template('./templates/dropTable/droptableconf',dbNames=dbNames,message=message,choosenDB=choosenDB,tablesList=tablesList)
        return output;
        
    else:
        
        dbmanager = databaseManager();
        dbNames = dbmanager.getDatabaseNames();
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        
        output = template('./templates/dropTable/dropTable',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
        return output;
    
#Manage table - Front Page
@route('/database/:choosenDB/manageTable/frontPage')
def manageTable(choosenDB):
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    
    output = template('./templates/manageTable/manageTableFront',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
    return output;

#Manage table
@route('/database/:choosenDB/manageTable/:tableName')
def manageTable(choosenDB,tableName):
    message = "Succesfull"
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
    table1 = table(choosenDB,tableName);
    
    if request.GET.get('add_col_btn','').strip():
        ColName = request.GET.get('ColName','').strip()
        colType = request.GET.get('colType','').strip()
        isNull = request.GET.get('isNull','').strip()
        isAI = request.GET.get('isAI','').strip()
        defaultValue = request.GET.get('defaultValue','').strip()        
        message = table1.addColumn(ColName,colType,isNull,defaultValue)
       
        
   
    tablesList = t1.getTablesNames();
    tColsInfo = table1.getAllColsInfo();
    dbNames = dbmanager.getDatabaseNames();
    
    output = template('./templates/manageTable/manageTable',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,tableName=tableName,tColsInfo=tColsInfo,message=message)
    return output;
    
    
#Manage Data - Front Page
@route('/database/:choosenDB/manageData/frontPage')
def manageDataforntPage(choosenDB):
    message = "Succesfull"
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    
    output = template('./templates/manageData/manageDataFrontPage',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,message=message)
    return output;
    
#Manage Data
@route('/database/:choosenDB/manageData/:tableName')
def manageData(choosenDB,tableName):
    message = "Succesfull"
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
    table1 = table(choosenDB,tableName);
    
    if request.GET.get('deleteCol','').strip():
        rowID = int(request.GET.get('deleteCol','').strip())
        table1.deleteRow(rowID)
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    tableColNames = table1.getColNames()
    tableData = table1.getData();
    
    output = template('./templates/manageData/manageData',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,tableName=tableName,message=message,tableColNames=tableColNames,tableData=tableData)
    return output;
    
#Manage Data - insertRow
@route('/database/:choosenDB/manageData/:tableName/insertRow')
def manageData(choosenDB,tableName):
    message = "Succesfull"
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
    table1 = table(choosenDB,tableName);
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    tableColNames = table1.getColNames()
    
    if request.GET.get('addRow','').strip():
        rowData = []
        for colName in tableColNames:
            rowData.append(request.GET.get("%s" %colName,'').strip())
        
        message = table1.insertRow(rowData)
        
        if message == "Succesfull":
            redirect("../%s" %tableName) 
    

    output = template('./templates/manageData/insertRow',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,tableName=tableName,message=message,tableColNames=tableColNames)
    return output;
    
    
#SQL Query
#isinstance(message,list)
@route('/database/:choosenDB/SQLQuery')
def SQLQuery(choosenDB):
    message = "start"
    query = ""
    dbmanager = databaseManager();
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    
    if request.GET.get('submit','').strip():
        query = request.GET.get('query','').strip()
        if query:
            message = t1.SQLQuery(query)
        
    output = template('./templates/SQLQuery/SQLQuery',dbNames=dbNames,choosenDB=choosenDB,message=message,query=query)
    return output;
    
@route('/SQLiteDatabases/<filename:path>')
def download(filename):
    return static_file(filename, root='SQLiteDatabases', download=filename)
    
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
debug(True)
run(reloader=True)
