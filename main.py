import sys
import math
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtSql
from pyqtgraph import PlotWidget
from myform import Ui_MainWindow


class calculations():
    Gravitation_Param = 398_600_000_000_000

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
        self.Engines_Thrust = (self.Gas_Flow_Speed * self.Gas_Mass) / (self.Fly_Time)
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
        foo = (self.Gas_Mass) / (3 * math.pi)
        self.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        self.Tank_CTR = round(self.Tank_Radius * 1.5)
        self.Body_lenght = round(500 * pow(self.Construct_Mass, 1 / 3))
        self.SP_Square = 0.5 * self.Engines_Power / (1.3 * 0.29 * 0.866)
        self.Payload_R = round(math.sqrt(self.Payload_Mass / (0.02 * 1.5 * math.pi)))
        self.EnginesCount = round(self.Engines_Thrust)

    def calc_master(self):
        self.Fly_Time = float(application.ui.lineEdit.text()) * 86400
        self.Start_Orbit_Height = float(application.ui.lineEdit_4.text())
        self.Start_Orbit_Inclination = float(application.ui.lineEdit_6.text()) * math.pi / 180
        self.Finally_Orbit_Height = float(application.ui.lineEdit_5.text())
        self.Finally_Orbit_Inclination = float(application.ui.lineEdit_7.text()) * math.pi / 180
        self.Start_SC_Mass = float(application.ui.lineEdit_2.text())
        self.Realitive_Construct_Mass = float(application.ui.lineEdit_12.text())
        self.SSS_Realitive_Mass = float(application.ui.lineEdit_11.text())
        self.Gas_Flow_Speed = float(application.ui.lineEdit_8.text())
        self.Engine_Specific_Mass = float(application.ui.lineEdit_9.text())
        self.Electro_Specific_Mass = float(application.ui.lineEdit_10.text())
        self.EFFICIENCY = float(application.ui.lineEdit_3.text())
        self.EFFICIENCY *= 0.01

        self.theor_calc()

        self.Initial_Speed = round(self.Initial_Speed)
        self.Gas_Flow_Speed = round(self.Gas_Flow_Speed)
        self.Electro_Mass = round(self.Electro_Mass, 3)
        self.Payload_Mass = round(self.Payload_Mass, 3)
        self.SSS_Mass = round(self.SSS_Mass, 3)
        self.Engines_Mass = round(self.Engines_Mass, 3)
        self.Construct_Mass = round(self.Construct_Mass, 3)
        self.Engines_Power = round(self.Engines_Power)
        self.Gas_Mass = round(self.Gas_Mass)
        self.Engines_Thrust = round(1000 * self.Engines_Thrust / 9.81, 3)
        self.Delta_velocity = round(self.Delta_velocity)

        application.ui.lineEdit_3.setText(str(self.EFFICIENCY * 100))
        application.ui.lineEdit_8.setText(str(self.Gas_Flow_Speed))
        application.ui.lineEdit_18.setText(str(self.Electro_Mass))
        application.ui.lineEdit_22.setText(str(self.Payload_Mass))
        application.ui.lineEdit_21.setText(str(self.SSS_Mass))
        application.ui.lineEdit_19.setText(str(self.Engines_Mass))
        application.ui.lineEdit_20.setText(str(self.Construct_Mass))
        application.ui.lineEdit_17.setText(str(self.Engines_Power / 1000))
        application.ui.lineEdit_16.setText(str(self.Engines_Thrust))
        application.ui.lineEdit_15.setText(str(self.Gas_Mass))
        application.ui.lineEdit_14.setText(str(self.Delta_velocity / 1000))
        application.ui.lineEdit_13.setText(str(self.Initial_Speed / 1000))


calcCore = calculations()


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_data()
        self.ui.pushButton.clicked.connect(calcCore.calc_master)
        self.ui.pushButton_2.clicked.connect(self.MSG)

    def msg_err(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("Ошибка открытия Базы Данных")
        messg.setText(str(self.db.lastError))
        x = messg.exec_()

    def load_data(self):

        self.db = QtSql.QSqlDatabase.addDatabase("QODBC")
        self.db.setDatabaseName(
            "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DSN='';DBQ=./engine.mdb")
        if self.db.open() == True:
            self.model = QtSql.QSqlTableModel(self, self.db)
            self.model.setTable("engine")
            self.model.select()
            self.ui.tableView.setModel(self.model)
        else:
            self.msg_err()

    def MSG(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("О Программе")
        messg.setText(" Разработчик: Хайруллин И.И. \n Самарский университета\n Кафедра космического машиностроения ")
        x = messg.exec_()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
