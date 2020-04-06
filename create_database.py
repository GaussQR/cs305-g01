from PyQt5 import QtSql, QtGui,QtWidgets



def createDB():
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('user.db')
	
   if not db.open():
      QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
         QtGui.qApp.tr("Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information "
            "how to build it.\n\n" "Click Cancel to exit."),
         QtGui.QMessageBox.Cancel)

      return False

   	
   query = QtSql.QSqlQuery()
	
   query.exec_("CREATE TABLE IF NOT EXISTS users(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,email Text,Password Varchar(6),mobile INTEGER,address TEXT)")   

   
   return True
	
print("here")
import sys
x=createDB()
print(x)