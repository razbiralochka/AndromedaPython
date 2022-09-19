from PyQt5 import QtSql


class Database():
    def __init__(self):
        self.__db = QtSql.QSqlDatabase.addDatabase("QODBC")
        self.__dbstate = False


    def connect(self, dbfilename):
        self.__db.setDatabaseName(
            "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DSN='';DBQ=" + dbfilename)
        self.__dbstate = self.__db.open()
        return self.__dbstate

    def get_last_error(self):
        return self.__db.lastError()

    def getdbstate(self):
        return self.__dbstate

    def get_db(self):
        return self.__db

    def getfromdb(self):
        pass