import sys
import math
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtSql
from pyqtgraph import PlotWidget
from myform import Ui_MainWindow


DBFILENAME = './engine.mdb'


class databaseClass():
    def __init__(self, dbfilename):
        self.__db = QtSql.QSqlDatabase.addDatabase("QODBC")
        self.__db.setDatabaseName(
            "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DSN='';DBQ=" + dbfilename)
        self.__dbstate = False
        if not self.__db.open():
            print('error db open')
            messg = QtWidgets.QMessageBox()
            messg.setWindowTitle("Ошибка открытия Базы Данных")
            messg.setText(str(self.__db.lastError))
            x = messg.exec_()
        else:
            self.__dbstate = True
            self.query = QtSql.QSqlQuery()

    def getdbstate(self):
        return self.__dbstate

    def get_db(self):
        return self.__db

    def getfromdb(self):
        pass



class calculations():
    Gravitation_Param = 398_600_000_000_000
    def set_Engines_Power(self, val):
        self.Engines_Power = val
    def set_Engines_Thrust(self, val):
        self.Engines_Thrust = val
    def set_Fly_Time(self, val):
        self.Fly_Time = val * 86400

    def set_Start_Orbit_Height(self, val):
        self.Start_Orbit_Height = val

    def set_Start_Orbit_Inclination(self, val):
        self.Start_Orbit_Inclination = val * math.pi / 180

    def set_Finally_Orbit_Height(self, val):
        self.Finally_Orbit_Height = val

    def set_Finally_Orbit_Inclination(self, val):
        self.Finally_Orbit_Inclination = val * math.pi / 180

    def set_Start_SC_Mass(self, val):
        self.Start_SC_Mass = val

    def set_Realitive_Construct_Mass(self, val):
        self.Realitive_Construct_Mass = val

    def set_SSS_Realitive_Mass(self, val):
        self.SSS_Realitive_Mass = val

    def set_Gas_Flow_Speed(self, val):
        self.Gas_Flow_Speed = val

    def set_Engine_Specific_Mass(self, val):
        self.Engine_Specific_Mass = val

    def set_Electro_Specific_Mass(self, val):
        self.Electro_Specific_Mass = val

    def set_efficency(self, val):
        self.EFFICIENCY = val * 0.01

    def db_calc(self):
#        database.db_read()
        self.Start_Orbit_Radius = (6371 + self.Start_Orbit_Height) * 1000
        self.Finnaly_Orbit_Radius = (6371 + self.Finally_Orbit_Height) * 1000
        self.Initial_Speed = math.sqrt(self.Gravitation_Param / self.Start_Orbit_Radius)
        self.Delta_velocity = self.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (self.Finally_Orbit_Inclination - self.Start_Orbit_Inclination)) +
            (self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius)
        )
        self.Gas_Mass = self.Start_SC_Mass * (
                1 - math.exp((-self.Delta_velocity) / self.Gas_Flow_Speed)
        )

        self.Construct_Mass = self.Realitive_Construct_Mass * self.Start_SC_Mass
        self.Engines_Mass = self.Engine_Specific_Mass * self.Engines_Thrust
        self.Electro_Mass = self.Electro_Specific_Mass * self.Engines_Power
        self.SSS_Mass = self.SSS_Realitive_Mass * self.Gas_Mass
        self.Payload_Mass = (self.Start_SC_Mass
                             - self.Gas_Mass
                             - self.Construct_Mass
                             - self.SSS_Mass
                             - self.Engines_Mass
                             - self.Electro_Mass)
        foo = self.Gas_Mass / (3 * math.pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.Engines_Power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
        self.EnginesCount = round(self.Engines_Thrust)

    def optimize_calc(self):
        pl_mass=0
        for i in range(18):
            database.index = i+1
            self.db_calc()
            if self.Payload_Mass > pl_mass:
                pl_mass = self.Payload_Mass
                bestindex = database.index
        database.index = bestindex
        self.db_calc()

    def theor_calc(self):
        self.Start_Orbit_Radius = (6371 + self.Start_Orbit_Height) * 1000
        self.Finnaly_Orbit_Radius = (6371 + self.Finally_Orbit_Height) * 1000
        self.Initial_Speed = math.sqrt(self.Gravitation_Param / self.Start_Orbit_Radius)
        self.Delta_velocity = self.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (self.Finally_Orbit_Inclination - self.Start_Orbit_Inclination)) +
            (self.Start_Orbit_Radius / self.Finnaly_Orbit_Radius)
        )
        self.Gas_Mass = self.Start_SC_Mass * (
                1 - math.exp((-self.Delta_velocity) / self.Gas_Flow_Speed)
        )
        self.Engines_Thrust = (self.Gas_Flow_Speed * self.Gas_Mass) / self.Fly_Time
        self.Engines_Power = (self.Engines_Thrust * self.Gas_Flow_Speed) / (2 * self.EFFICIENCY)
        self.Construct_Mass = self.Realitive_Construct_Mass * self.Start_SC_Mass
        self.Engines_Mass = self.Engine_Specific_Mass * self.Engines_Thrust
        self.Electro_Mass = self.Electro_Specific_Mass * self.Engines_Power
        self.SSS_Mass = self.SSS_Realitive_Mass * self.Gas_Mass
        self.Payload_Mass = (self.Start_SC_Mass
                             - self.Gas_Mass
                             - self.Construct_Mass
                             - self.SSS_Mass
                             - self.Engines_Mass
                             - self.Electro_Mass)
        foo = self.Gas_Mass / (3 * math.pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.Engines_Power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
        self.EnginesCount = round(self.Engines_Thrust)

    def calc_master(self, mode):
        if mode == 1:
            self.theor_calc()
        elif mode == 2:
            self.db_calc()
        elif mode == 3:
            self.optimize_calc()

        self.EFFICIENCY = round(self.EFFICIENCY*100)
        self.Initial_Speed = round(self.Initial_Speed, 3)
        self.Gas_Flow_Speed = round(self.Gas_Flow_Speed, 3)
        self.Electro_Mass = round(self.Electro_Mass, 3)
        self.Payload_Mass = round(self.Payload_Mass, 3)
        self.SSS_Mass = round(self.SSS_Mass, 3)
        self.Engines_Mass = round(self.Engines_Mass, 3)
        self.Construct_Mass = round(self.Construct_Mass, 3)
        self.Engines_Power = round(self.Engines_Power)
        self.Gas_Mass = round(self.Gas_Mass)
        self.Engines_Thrust = round(1000 * self.Engines_Thrust / 9.81, 3)
        self.Delta_velocity = round(self.Delta_velocity)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.launch_calc)
        self.ui.pushButton_2.clicked.connect(self.MSG)


    def associateCalcCore(self, calcCore):
        self.calcCore = calcCore

    def associateDatabase(self, db):
        self.db = db
        self.db_model()
        self.ui.tableView.doubleClicked.connect(self.readfromdatabase)

    def readfromdatabase(self):

        for item in self.ui.tableView.selectedIndexes():
            self.selectedEngine = str(item.row() + 1)

            print(self.ui.tableView.model().index(item.row() + 1, 1).data())
            print(self.ui.tableView.model().index(item.row() + 1, 2).data())
            print(self.ui.tableView.model().index(item.row() + 1, 3).data())
            print(self.ui.tableView.model().index(item.row() + 1, 4).data())
            print(self.ui.tableView.model().index(item.row() + 1, 5).data())
            print(self.ui.tableView.model().index(item.row() + 1, 6).data())

            # if self.ui.radioButton_3.isChecked():
            #     self.selectedEngine = str(self.index)
            #
            # self.ui.lineEdit_8.setText(str(float(query.value(3)) * 1000.0))
            # self.ui.lineEdit_16.setText(str(float(query.value(2)) * 0.001))
            # self.ui.lineEdit_17.setText(str(float(query.value(4)) * 1000.0))
            # self.ui.lineEdit_3.setText(str(float(query.value(5))))
            self.ui.lineEdit_23.setText(self.ui.tableView.model().index(item.row() + 1, 1).data())


    def MSG(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("О Программе")
        messg.setText("Хайруллин И.И.")
        x = messg.exec_()

    def db_model(self):
        if self.db.getdbstate():
            self.model = QtSql.QSqlTableModel(self, self.db.get_db())
            self.model.setTable("engine")
            self.model.select()
            self.ui.tableView.setModel(self.model)

    def postresult(self):
        self.ui.lineEdit_3.setText(str(self.calcCore.EFFICIENCY))
        self.ui.lineEdit_8.setText(str(self.calcCore.Gas_Flow_Speed))
        self.ui.lineEdit_18.setText(str(self.calcCore.Electro_Mass))
        self.ui.lineEdit_22.setText(str(self.calcCore.Payload_Mass))
        self.ui.lineEdit_21.setText(str(self.calcCore.SSS_Mass))
        self.ui.lineEdit_19.setText(str(self.calcCore.Engines_Mass))
        self.ui.lineEdit_20.setText(str(self.calcCore.Construct_Mass))
        self.ui.lineEdit_17.setText(str(self.calcCore.Engines_Power / 1000))
        self.ui.lineEdit_16.setText(str(self.calcCore.Engines_Thrust))
        self.ui.lineEdit_15.setText(str(self.calcCore.Gas_Mass))
        self.ui.lineEdit_14.setText(str(self.calcCore.Delta_velocity / 1000))
        self.ui.lineEdit_13.setText(str(self.calcCore.Initial_Speed / 1000))


    def launch_calc(self):
        self.calcCore.set_Fly_Time(
            float(self.ui.lineEdit.text())
        )

        self.calcCore.set_Start_Orbit_Height(
            float(self.ui.lineEdit_4.text())
        )
        self.calcCore.set_Start_Orbit_Inclination(
            float(self.ui.lineEdit_6.text())
        )
        self.calcCore.set_Finally_Orbit_Height(
            float(self.ui.lineEdit_5.text())
        )
        self.calcCore.set_Finally_Orbit_Inclination(
            float(self.ui.lineEdit_7.text())
        )
        self.calcCore.set_Start_SC_Mass(
            float(self.ui.lineEdit_2.text())
        )
        self.calcCore.set_Realitive_Construct_Mass(
            float(self.ui.lineEdit_12.text())
        )
        self.calcCore.set_SSS_Realitive_Mass(
            float(self.ui.lineEdit_11.text())
        )
        self.calcCore.set_Gas_Flow_Speed(
            float(self.ui.lineEdit_8.text())
        )
        self.calcCore.set_Engine_Specific_Mass(
            float(self.ui.lineEdit_9.text())
        )
        self.calcCore.set_Electro_Specific_Mass(
            float(self.ui.lineEdit_10.text())
        )
        self.calcCore.set_efficency(
            float(self.ui.lineEdit_3.text())
        )

        if self.ui.radioButton.isChecked():
            mode = 1
        if self.ui.radioButton_2.isChecked():
            mode = 2
        if self.ui.radioButton_3.isChecked():
            mode = 3
        self.calcCore.calc_master(mode)

        self.postresult()


def main():
    calcCore = calculations()
    database = databaseClass(DBFILENAME)

    app = QtWidgets.QApplication([])
    application = mywindow()
    application.associateCalcCore(calcCore)
    application.associateDatabase(database)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
