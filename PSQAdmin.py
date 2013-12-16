import sqlite3
import os
from bottle import route, run, debug, template, request, validate, static_file, error,redirect
from bottle import default_app
from PSQALibrary.databaseManager import * 
from PSQALibrary.database1 import * 
from PSQALibrary.table import * 
from PSQALibrary.indexManager import *
from PSQALibrary.viewManager import *




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
    
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    
    
    isValid = t1.isValidSQliteDatase()
    if isValid:
        tablesList = t1.getTablesNames();
        output = template('./templates/index/database',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
        return output;
    else:
        output = template('./templates/index/indexInvalidDatabase',dbNames=dbNames,choosenDB=choosenDB)
        return output;
        
    
    
#upload databse - page1
@route('/uploadDB')
def uploadDB():
    message = "start"
    dbmanager = databaseManager();
    dbNames = dbmanager.getDatabaseNames();
    output = template('./templates/uploadDB/uploadDB',dbNames=dbNames,message=message)
    return output;
    
#upload database - page2
@route('/uploadDB2', method='POST')
def uploadDB2():
    dbmanager = databaseManager();
    dbNames = dbmanager.getDatabaseNames();
    message = "done"
    
    data = request.files.data
    if data and data.file:
        raw = data.file.read()
        filename = data.filename
        if os.path.exists("./SQLiteDatabases/%s" %(filename)):
            message = "The database already exist"
        else:
            if ".db" in filename:
                with open("./SQLiteDatabases/%s" %(filename),'w') as open_file:
                    open_file.write(raw)  
            else:
                message = "Not a valid sqlite database file"
    else:
        message =  "You missed a field."
    
    output = template('./templates/uploadDB/uploadDB',dbNames=dbNames,message=message)
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
            try:
                dbmanager.createDatabase(newDBName)
                message="The database was created succesfully"
            except:
                message = "Error: Invalid database name"
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
        
#Download database
@route('/SQLiteDatabases/<filename:path>')
def download(filename):
    return static_file(filename, root='SQLiteDatabases', download=filename)
    
    
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
        if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
            redirect("/error")
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
        if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
            redirect("/error")
        dbNames = dbmanager.getDatabaseNames();
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        
        t1 = database1(choosenDB)
        tablesList = t1.getTablesNames();
        
        output = template('./templates/dropTable/dropTable',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
        return output;
    
#Manage table - Front Page
@route('/database/:choosenDB/manageTable/frontPage')
def manageTableFront(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
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
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
    table1 = table(choosenDB,tableName);
    
    if request.GET.get('deleteCol','').strip():
        message = table1.deleteCol(request.GET.get('deleteCol','').strip())
    
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
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
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
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
    table1 = table(choosenDB,tableName);
    
    if request.GET.get('deleteCol','').strip():
        rowID = int(request.GET.get('deleteCol','').strip())
        table1.deleteRow(rowID)
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    tableColNames = table1.getColNames()
    
    pageNo = request.GET.get('pageNo','').strip()
    if pageNo:
        pageNo = int(pageNo)
        tableData = table1.getData((pageNo-1)*30);
    else:
        pageNo = 1
        tableData = table1.getData(0);
        
    noOfPages = (table1.getNumberofPages()/30) + 1
    
    output = template('./templates/manageData/manageData',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,tableName=tableName,message=message,tableColNames=tableColNames,tableData=tableData,noOfPages=noOfPages,pageNo=pageNo)
    return output;
    
#Manage Data - insertRow
@route('/database/:choosenDB/manageData/:tableName/insertRow')
def manageDataInsert(choosenDB,tableName):
    message = "Succesfull"
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
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
    
#Manage Data - updateRow
@route('/database/:choosenDB/manageData/:tableName/editRow/:rowID')
def updateRow(choosenDB,tableName,rowID):
    message = ""
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
    table1 = table(choosenDB,tableName);
   
    tablesList = t1.getTablesNames();
    dbNames = dbmanager.getDatabaseNames();
    tableColNames = table1.getColNames()
    
    rowData = table1.getRowData(rowID)
    
    if request.GET.get('updateRow','').strip():
        rowData = []
        for colName in tableColNames:
            rowData.append([colName,request.GET.get("%s" %colName,'').strip()])
        
        message = table1.updateRow(rowData,rowID)
        #return message
        
        if message == "Succesfull":
            message = "The record was updated successfully"
    
    output = template('./templates/manageData/editRow',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,tableName=tableName,message=message,rowData=rowData,rowID=rowID)
    return output;
    
    
#SQL Query
@route('/database/:choosenDB/SQLQuery')
def SQLQuery(choosenDB):
    message = "start"
    query = ""
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    
    if request.GET.get('submit','').strip():
        query = request.GET.get('query','').strip()
        if query:
            message = t1.SQLQuery(query)
        
    output = template('./templates/SQLQuery/SQLQuery',dbNames=dbNames,choosenDB=choosenDB,message=message,query=query)
    return output;
    
#Export Data - Front page
@route('/database/:choosenDB/exportData')
def exportData(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    
    output = template('./templates/exportData/exportData',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
    return output;
    
#Export Data - Download File
@route('/database/:choosenDB/exportData/<tableName>.csv')
def exportDataDownload(choosenDB,tableName):
    table1 = table(choosenDB,tableName);
    table1.generateCSVFile()
    return static_file(tableName+".csv", root='temp/exportFiles', download=tableName+".csv")
    
    
    
#Import data - Front page
@route('/database/:choosenDB/importData')
def importData(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();

    output = template('./templates/importData/importData',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList)
    return output;
    
#import data - upload and import
@route('/database/:choosenDB/importData/:tableName/upload', method='POST')
def do_upload(choosenDB,tableName):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    table1 = table(choosenDB,tableName);
    
    data = request.files.data
    if data and data.file:
        raw = data.file.read()
        filename = data.filename
        with open("./temp/importFiles/%s" %(filename),'w') as open_file:
            open_file.write(raw)
        message = table1.importCSV("./temp/importFiles/%s" %(filename))   
    else:
        message =  "You missed a field."
    
    output = template('./templates/importData/importDataUpload',dbNames=dbNames,choosenDB=choosenDB,tablesList=tablesList,message = message)
    return output;
    

#Create Index - frontPage
@route('/database/:choosenDB/createIndex')
def createIndexFront(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    
    output = template('./templates/createIndex/createIndex',dbNames=dbNames,choosenDB=choosenDB,tablesList = tablesList)
    return output;
    
    
#Create Index - table is chosen
@route('/database/:choosenDB/createIndex/:tableName')
def createIndexTableChosen(choosenDB,tableName):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    if not t1.doesTableExist(tableName):
        redirect("/error")
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    table1 = table(choosenDB,tableName);
    tableColNames = table1.getColNames()
    
    output = template('./templates/createIndex/createIndexTC',dbNames=dbNames,choosenDB=choosenDB,tablesList = tablesList,tableName=tableName,tableColNames=tableColNames)
    return output;
    
#Create Index - get the index info and create it
@route('/database/:choosenDB/createIndex/:tableName', method='POST')
def createIndexConfirm(choosenDB,tableName):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB);
    if not t1.doesTableExist(tableName):
        redirect("/error")
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    table1 = table(choosenDB,tableName);
    tableColNames = table1.getColNames()
    
    index_name = request.POST.get('IndexName','').strip()
    index_tbl_name = request.POST.get('tableN','').strip()
    index_col_list = request.POST.getall('col')
    
    indexManager1 = indexManager(choosenDB)
    message = indexManager1.createIndex(index_name,index_tbl_name,index_col_list)
    
    output = template('./templates/createIndex/createIndexConf',dbNames=dbNames,choosenDB=choosenDB,tablesList = tablesList,tableName=tableName,tableColNames=tableColNames,message = message)
    return output;
    
#drop Index
@route('/database/:choosenDB/dropIndex')
def dropIndex(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    
    indexManager1 = indexManager(choosenDB)
    
    if(request.GET.get('dropIndex','').strip()):
        indexManager1.dropIndex(request.GET.get('dropIndex','').strip())
    
    indInfo = indexManager1.getAllIndicesInfo()
    
    output = template('./templates/dropIndex/dropIndex',dbNames=dbNames,choosenDB=choosenDB,indInfo=indInfo)
    return output;
    
#Create View - frontPage
@route('/database/:choosenDB/createView')
def createView(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    
    output = template('./templates/createView/createView',dbNames=dbNames,choosenDB=choosenDB,tablesList = tablesList)
    return output;
    
#Create View - second Page
@route('/database/:choosenDB/createView2')
def createView2(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    
    tableName = request.GET.get('tableN','').strip()
    viewName = request.GET.get('ViewName','').strip()
    table1 = table(choosenDB,tableName);
    tableColNames = ",".join(table1.getColNames())
    
    Viewquery = "CREATE VIEW %s AS \nSELECT %s \nFROM %s" %(viewName,tableColNames,tableName)
      
    output = template('./templates/createView/createView2',dbNames=dbNames,choosenDB=choosenDB,Viewquery=Viewquery)
    return output;
    
#Create View - third Page
@route('/database/:choosenDB/createView3')
def createView3(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    tablesList = t1.getTablesNames();
    
    Viewquery = request.GET.get('Viewquery','').strip()
    message = t1.SQLQuery(Viewquery)
    
    output = template('./templates/createView/createView3',dbNames=dbNames,choosenDB=choosenDB,Viewquery=Viewquery,message = message)
    return output;
    
#Manage View 
@route('/database/:choosenDB/manageView')
def manageView(choosenDB):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    viewmanager1 = viewManager(choosenDB)
    
    viewName = request.GET.get('dropView','').strip()
    if viewName:
        viewmanager1.dropView(viewName)
        
    viewNames = viewmanager1.getViewNames()
    
    output = template('./templates/manageView/manageView',dbNames=dbNames,choosenDB=choosenDB,viewNames=viewNames)
    return output;
    
    
#Edit View 
@route('/database/:choosenDB/editView/:viewName')
def editView(choosenDB,viewName):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    viewmanager1 = viewManager(choosenDB)
    message = "start"
    
    sqlStat = viewmanager1.getViewSQL(viewName)
        
    output = template('./templates/manageView/editView',dbNames=dbNames,choosenDB=choosenDB,sqlStat=sqlStat,message=message,viewName=viewName)
    return output;
    
#Edit View2 
@route('/database/:choosenDB/editView2/:viewName')
def editView2(choosenDB,viewName):
    dbmanager = databaseManager();
    if not dbmanager.doesDBExists(choosenDB.replace('.db', '')):
        redirect("/error")
    t1 = database1(choosenDB)
    dbNames = dbmanager.getDatabaseNames();
    viewmanager1 = viewManager(choosenDB)
    message = "start"
    
    sqlStat = request.GET.get('updatedSQLStat','').strip()
    message = viewmanager1.updateViewSQL(viewName,sqlStat)
        
    output = template('./templates/manageView/editView2',dbNames=dbNames,choosenDB=choosenDB,sqlStat=sqlStat,message=message,viewName=viewName)
    return output;
    
    
#upload database
@route('/database/uploadDatabase', method='POST')
def uploadDatabase():    
    data = request.files.data
    if data and data.file:
        raw = data.file.read()
        filename = data.filename
        with open("./temp/importFiles/%s" %(filename),'w') as open_file:
            open_file.write(raw)
        message = "The database were succesfully uploaded"   
    else:
        message =  "You missed a field."
        
    return message
    
    output = template('./templates/importData/importDataUpload',message = message)
    return output;

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')
    
@error(404)
def error404(error):
    dbmanager = databaseManager();
    dbNames = dbmanager.getDatabaseNames();
    output = template('./templates/error/pageNoteFound',dbNames=dbNames)
    return output;

    
    
debug(True)
run(host='0.0.0.0',reloader=True,port =8080)
