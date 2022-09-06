import sys
import math
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtSql
from pyqtgraph import PlotWidget
from myform import Ui_MainWindow

class theorCalcClass():
    def theor_calc(self):
        calcCore.Start_Orbit_Radius = (6371 + calcCore.Start_Orbit_Height) * 1000
        calcCore.Finnaly_Orbit_Radius = (6371 + calcCore.Finally_Orbit_Height) * 1000
        calcCore.Initial_Speed = math.sqrt(calcCore.Gravitation_Param / calcCore.Start_Orbit_Radius)
        calcCore.Delta_velocity = calcCore.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(calcCore.Start_Orbit_Radius / calcCore.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (calcCore.Finally_Orbit_Inclination - calcCore.Start_Orbit_Inclination)) +
            (calcCore.Start_Orbit_Radius / calcCore.Finnaly_Orbit_Radius)
        )
        calcCore.Gas_Mass = calcCore.Start_SC_Mass * (
                1 - math.exp((-calcCore.Delta_velocity) / calcCore.Gas_Flow_Speed)
        )
        calcCore.Engines_Thrust = (calcCore.Gas_Flow_Speed * calcCore.Gas_Mass) / calcCore.Fly_Time
        calcCore.Engines_Power = (calcCore.Engines_Thrust * calcCore.Gas_Flow_Speed) / (2 * calcCore.EFFICIENCY)
        calcCore.Construct_Mass = calcCore.Realitive_Construct_Mass * calcCore.Start_SC_Mass
        calcCore.Engines_Mass = calcCore.Engine_Specific_Mass * calcCore.Engines_Thrust
        calcCore.Electro_Mass = calcCore.Electro_Specific_Mass * calcCore.Engines_Power
        calcCore.SSS_Mass = calcCore.SSS_Realitive_Mass * calcCore.Gas_Mass
        calcCore.Payload_Mass = (calcCore.Start_SC_Mass
                             - calcCore.Gas_Mass
                             - calcCore.Construct_Mass
                             - calcCore.SSS_Mass
                             - calcCore.Engines_Mass
                             - calcCore.Electro_Mass)
        foo = calcCore.Gas_Mass / (3 * math.pi)
        calcCore.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        calcCore.Tank_CTR = round(calcCore.Tank_Radius * 1.5)
        calcCore.Body_lenght = round(500 * pow(calcCore.Construct_Mass, 1 / 3))
        calcCore.SP_Square = 0.5 * calcCore.Engines_Power / (1.3 * 0.29 * 0.866)
        calcCore.Payload_R = round(math.sqrt(calcCore.Payload_Mass / (0.02 * 1.5 * math.pi)))
        calcCore.EnginesCount = round(calcCore.Engines_Thrust)
class databaseClass():
    def db_init(self, obj):

        db = QtSql.QSqlDatabase.addDatabase("QODBC")
        db.setDatabaseName(
            "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DSN='';DBQ=./engine.mdb")
        if not db.open():
            print('error db open')
            messg = QtWidgets.QMessageBox()
            messg.setWindowTitle("Ошибка открытия Базы Данных")
            messg.setText(str(db.lastError))
            x = messg.exec_()
        self.model = QtSql.QSqlTableModel(obj, db)
        self.model.setTable("engine")
        self.model.select()
        obj.ui.tableView.setModel(self.model)

    def db_read(self):
        query = QtSql.QSqlQuery()

        for item in application.ui.tableView.selectedIndexes():
            self.selectedEngine = str(item.row() + 1)
        query.exec("SELECT * FROM engine WHERE Код = " + self.selectedEngine)

        while query.next():
            name = str(query.value(1))
            calcCore.Engines_Thrust = float(query.value(2)) * 0.001
            calcCore.Gas_Flow_Speed = float(query.value(3)) * 1000.0
            calcCore.Engines_Power = float(query.value(4)) * 1000.0
            calcCore.EFFICIENCY = float(query.value(5)) * 0.01
            application.ui.lineEdit_23.setText(name)


    def db_calc(self):
       # self.db_read()
        calcCore.Start_Orbit_Radius = (6371 + calcCore.Start_Orbit_Height) * 1000
        calcCore.Finnaly_Orbit_Radius = (6371 + calcCore.Finally_Orbit_Height) * 1000
        calcCore.Initial_Speed = math.sqrt(calcCore.Gravitation_Param / calcCore.Start_Orbit_Radius)
        calcCore.Delta_velocity = calcCore.Initial_Speed * math.sqrt(
            1 - 2 * math.sqrt(calcCore.Start_Orbit_Radius / calcCore.Finnaly_Orbit_Radius) *
            math.cos((math.pi / 2) * (calcCore.Finally_Orbit_Inclination - calcCore.Start_Orbit_Inclination)) +
            (calcCore.Start_Orbit_Radius / calcCore.Finnaly_Orbit_Radius)
        )
        calcCore.Gas_Mass = calcCore.Start_SC_Mass * (
                1 - math.exp((-calcCore.Delta_velocity) / calcCore.Gas_Flow_Speed)
        )

        calcCore.Construct_Mass = calcCore.Realitive_Construct_Mass * calcCore.Start_SC_Mass
        calcCore.Engines_Mass = calcCore.Engine_Specific_Mass * calcCore.Engines_Thrust
        calcCore.Electro_Mass = calcCore.Electro_Specific_Mass * calcCore.Engines_Power
        calcCore.SSS_Mass = calcCore.SSS_Realitive_Mass * calcCore.Gas_Mass
        calcCore.Payload_Mass = (calcCore.Start_SC_Mass
                             - calcCore.Gas_Mass
                             - calcCore.Construct_Mass
                             - calcCore.SSS_Mass
                             - calcCore.Engines_Mass
                             - calcCore.Electro_Mass)
        foo = calcCore.Gas_Mass / (3 * math.pi)
        calcCore.Tank_Radius = 100 * round(pow(foo, 1 / 3))
        calcCore.Tank_CTR = round(calcCore.Tank_Radius * 1.5)
        calcCore.Body_lenght = round(500 * pow(calcCore.Construct_Mass, 1 / 3))
        calcCore.SP_Square = 0.5 * calcCore.Engines_Power / (1.3 * 0.29 * 0.866)
        calcCore.Payload_R = round(math.sqrt(calcCore.Payload_Mass / (0.02 * 1.5 * math.pi)))
        calcCore.EnginesCount = round(calcCore.Engines_Thrust)

    #def optimize_calc(self):





class calculations():
    Gravitation_Param = 398_600_000_000_000


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



        if application.ui.radioButton.isChecked():
            theorCalc.theor_calc()
        if application.ui.radioButton_2.isChecked():
            database.db_calc()


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


        application.ui.lineEdit_3.setText(str(self.EFFICIENCY))
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
theorCalc = theorCalcClass()
database = databaseClass()

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        database.db_init(self)

        self.ui.pushButton.clicked.connect(calcCore.calc_master)
        self.ui.pushButton_2.clicked.connect(self.MSG)
        self.ui.tableView.doubleClicked.connect(database.db_read)

    def MSG(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("О Программе")
        messg.setText("Хайруллин И.И.")
        x = messg.exec_()


app = QtWidgets.QApplication([])


application = mywindow()




application.show()
sys.exit(app.exec())