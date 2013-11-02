import sqlite3
import cgi
import os


class databaseManager:

    #intilaize the class object with the database name
    def __init__(self):
        pass
        
        
    # create a new database (done)
    def createDatabase(self,databaseName):
        con = sqlite3.connect("./SQLiteDatabases/%s.db" %databaseName)
        
    #drop a database (done)
    def dropDatabase(self,databaseName):
        os.remove("./SQLiteDatabases/%s" %databaseName)
        
    # return a list of the database names (done)
    def getDatabaseNames(self):
        fileNamesList = []
        for files in os.listdir("./SQLiteDatabases/"):
            if files.endswith(".db"):
                fileNamesList.append(files);
        return fileNamesList;
        
    # check if the database already exists (done)
    def doesDBExists(self,databaseName):
        for files in os.listdir("./SQLiteDatabases/"):
            if files == ("%s.db" %databaseName):
                return True;
        return False
        
        

#t1 = databaseManager();
#t1.dropDatabase("ibrary2.db")
#fileNames = t1.getDatabaseNames();
#print fileNames;
#t1.createDatabase("ibrary2.db");

#print t1.getTablesNames()




























    
