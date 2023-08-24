import sys
import math
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtSql
from myform import Ui_MainWindow
from numba import njit

class RungeKuttaClass():
    Gravitation_Param = 398_600_000_000_000
    def __init__(self):
        self.t_list = list()
        self.inc_list = list()
        self.r_list = list()
        self.time = float()
        self.radius = float()
        self.inc = float()
        self.u_ang = 0
        self.vel= 0

    def f_psi(self):
        U_ANG = self.u_ang
        R_0 = calcCore.Start_Orbit_Radius
        R_F = calcCore.Finnaly_Orbit_Radius
        INC_0 = calcCore.Start_Orbit_Inclination
        INC_F = calcCore.Finally_Orbit_Inclination
        VEL_0 = calcCore.Initial_Speed
        V_X = self.vel
        psi_max = math.atan(math.sin(math.pi*(INC_F-INC_0)/2)/
                            math.sqrt(R_F/R_0)*1/(1-math.cos(math.pi*(INC_F-INC_0)/2)/
                            math.sqrt(R_F/R_0)-V_X/VEL_0*
                            math.sqrt(1-2*math.cos(math.pi*(INC_F-INC_0)/2)/
                            math.sqrt(R_F/R_0)+R_0/R_F)))

        if INC_F < INC_0:
            if (psi_max < 0):
                res = psi_max*np.sign(math.cos(U_ANG))
            if (psi_max > 0):
                res = (psi_max - math.pi)*np.sign(math.cos(U_ANG))
        if  INC_F > INC_0:
            if (psi_max > 0):
                res = psi_max*np.sign(math.cos(U_ANG))
            if (psi_max < 0):
                res = (psi_max + math.pi)*np.sign(math.cos(U_ANG))
        return res

    def x_acc(self):
        INITIAL_ACCELERATION = calcCore.Engines_Thrust/calcCore.Start_SC_Mass

        res = INITIAL_ACCELERATION*math.cos(self.f_psi())*\
              math.exp(self.vel/calcCore.Gas_Flow_Speed)
        return res
    def z_acc(self):
        INITIAL_ACCELERATION = calcCore.Engines_Thrust / calcCore.Start_SC_Mass

        res = INITIAL_ACCELERATION*math.sin(self.f_psi())*\
              math.exp(self.vel/calcCore.Gas_Flow_Speed)
        return res

    def dr(self, t, r, inc, u_ang,vel):
        res = 2*self.x_acc()*\
              math.sqrt((r**3)/self.Gravitation_Param)
        return res

    def di(self, t, r, inc, u_ang, vel):
        res = self.z_acc()*math.sqrt(self.radius/self.Gravitation_Param)*\
              math.cos(u_ang)

        return res

    def du(self, t, r, inc, u_ang, vel):
        res = math.sqrt(self.Gravitation_Param/(r**3))
        return res

    def dV(self, t, r, inc, u_ang, vel):
        res = math.sqrt((self.x_acc()**2)+
                        (self.z_acc()**2))
        return res


    def RK4(self):
        self.time = 0
        self.radius = calcCore.Start_Orbit_Radius
        self.inc = calcCore.Start_Orbit_Inclination

        k = np.zeros((4, 4))
        h = 100

        while self.time < calcCore.Fly_Time:

            k[0][0] = h * self.dr(self.time, self.radius, self.inc, self.u_ang, self.vel)
            k[1][0] = h * self.di(self.time, self.radius, self.inc, self.u_ang, self.vel)
            k[2][0] = h * self.du(self.time, self.radius, self.inc, self.u_ang, self.vel)
            k[3][0] = h * self.dV(self.time, self.radius, self.inc, self.u_ang, self.vel)

            k[0][1] = h * self.dr(self.time + h / 2.0, self.radius + k[0][0] / 2.0, self.inc + k[1][0] / 2.0,
                             self.u_ang + k[2][0] / 2.0, self.vel + k[3][0] / 2.0)
            k[1][1] = h * self.di(self.time + h / 2.0, self.radius + k[0][0] / 2.0, self.inc + k[1][0] / 2.0,
                             self.u_ang + k[2][0] / 2.0, self.vel + k[3][0] / 2.0)
            k[2][1] = h * self.du(self.time + h / 2.0, self.radius + k[0][0] / 2.0, self.inc + k[1][0] / 2.0,
                             self.u_ang + k[2][0] / 2.0, self.vel + k[3][0] / 2.0)
            k[3][1] = h * self.dV(self.time + h / 2.0, self.radius + k[0][0] / 2.0, self.inc + k[1][0] / 2.0,
                             self.u_ang + k[2][0] / 2.0, self.vel + k[3][0] / 2.0)

            k[0][2] = h * self.dr(self.time + h / 2.0, self.radius + k[0][1] / 2.0, self.inc + k[1][1] / 2.0,
                             self.u_ang + k[2][1] / 2.0, self.vel + k[3][1] / 2.0)
            k[1][2] = h * self.di(self.time + h / 2.0, self.radius + k[0][1] / 2.0, self.inc + k[1][1] / 2.0,
                             self.u_ang + k[2][1] / 2.0, self.vel + k[3][1] / 2.0)
            k[2][2] = h * self.du(self.time + h / 2.0, self.radius + k[0][1] / 2.0, self.inc + k[1][1] / 2.0,
                             self.u_ang + k[2][1] / 2.0, self.vel + k[3][1] / 2.0)
            k[3][2] = h * self.dV(self.time + h / 2.0, self.radius + k[0][1] / 2.0, self.inc + k[1][1] / 2.0,
                             self.u_ang + k[2][1] / 2.0, self.vel + k[3][1] / 2.0)

            k[0][3] = h * self.dr(self.time + h, self.radius + k[0][2], self.inc + k[1][2], self.u_ang + k[2][2], self.vel + k[3][2]);
            k[1][3] = h * self.di(self.time + h, self.radius + k[0][2], self.inc + k[1][2], self.u_ang + k[2][2], self.vel + k[3][2]);
            k[2][3] = h * self.du(self.time + h, self.radius + k[0][2], self.inc + k[1][2], self.u_ang + k[2][2], self.vel + k[3][2]);
            k[3][3] = h * self.dV(self.time + h, self.radius + k[0][2], self.inc + k[1][2], self.u_ang + k[2][2], self.vel + k[3][2]);

            self.inc_list.append(180*self.inc/math.pi)
            self.r_list.append(self.radius/1000)
            self.t_list.append(self.time/86000)

            self.time += h
            self.radius += (k[0][0]+2.0*k[0][1]+2.0*k[0][2]+k[0][3])/6.0
            self.inc += (k[1][0]+2.0*k[1][1]+2.0*k[1][2]+k[1][3])/6.0
            self.u_ang += (k[2][0]+2.0*k[2][1]+2.0*k[2][2]+k[2][3])/6.0
            self.vel += (k[3][0]+2.0*k[3][1]+2.0*k[3][2]+k[3][3])/6.0
        pen = pg.mkPen(color=(0, 0, 0), width=2)
        application.ui.widget_2.plotItem.plot(self.t_list , self.inc_list ,pen=pen)
        application.ui.widget_3.plotItem.plot(self.t_list , self.r_list, pen=pen)
        self.inc = round(180*self.inc/math.pi, 2)
        self.radius = round(self.radius/1000 , 2)

        application.ui.label_31.setText("Зависимость наклонения орбиты (град) от времени (сут). Конечное наклонение: "
                                        + str(self.inc) + " град")
        application.ui.label_32.setText("Зависимость радиуса орбиты (км) от времени (сут). Конечный радиус: "
                                        + str(self.radius)+ " км")



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
        self.selectedEngine = 0
        obj.ui.tableView.setModel(self.model)

    def db_read(self):
        query = QtSql.QSqlQuery()

        self.selectedEngine = str(self.selectedEngine)
        query.exec("SELECT * FROM engine WHERE Код = " + self.selectedEngine)

        while query.next():
            name = str(query.value(1))
            calcCore.Engines_Thrust = float(query.value(2)) * 0.001
            calcCore.Gas_Flow_Speed = float(query.value(3)) * 1000.0
            calcCore.Engines_Power = float(query.value(4)) * 1000.0
            calcCore.EFFICIENCY = float(query.value(5)) * 0.01
            application.ui.lineEdit_23.setText(name)

    def db_calc(self):

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

    def optimize_calc(self):
        best = 0
        max_layload = 0
        for i in range(18):
            self.selectedEngine = i + 1
            self.db_read()
            self.db_calc()
            if calcCore.Payload_Mass > max_layload:
                max_layload = calcCore.Payload_Mass
                best = i

        self.selectedEngine = best + 1
        self.db_read()
        self.db_calc()


class calcClass():

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
            self.theor_calc()
        if application.ui.radioButton_2.isChecked():
            database.db_read()
            database.db_calc()
        if application.ui.radioButton_3.isChecked():
            database.optimize_calc()


        rk_core.RK4()

        self.EFFICIENCY = round(self.EFFICIENCY * 100)
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

        foo = calcCore.Gas_Mass / (3 * math.pi)
        Tank_Radius = 100 * round(pow(foo, 1 / 3)/8)
        Tank_CTR = round(Tank_Radius * 1.5)
        Body_lenght = round(50 * pow(calcCore.Construct_Mass, 1 / 3))
        SP_Square = 0.5 * calcCore.Engines_Power / (1.3 * 0.29 * 0.866)
        SP_W = round(math.sqrt(SP_Square) / 2)
        SP_L = SP_W * 4;
        Payload_R = round(math.sqrt(calcCore.Payload_Mass / (0.02 * 1.5 * math.pi)))
        Payload_L = Payload_R * 1.5
        EnginesCount = round(calcCore.Engines_Thrust/98.1)
        EnginePlateRadius = round(Body_lenght * math.sqrt(2) / 2);
        EngineRadius = 25
        EngineLenght = 30
        Engine_CTR = 180
        export = np.array([Body_lenght,
                           Body_lenght,
                           Body_lenght,
                           Tank_Radius,
                           Tank_CTR,
                           EnginePlateRadius,
                           EngineRadius,
                           EngineLenght,
                           Engine_CTR,
                           EnginesCount,
                           Payload_R,
                           Payload_L,
                           SP_W,
                           SP_L])
        np.savetxt("Data.csv", export, fmt='% 4d')
        application.save_msg()
calcCore = calcClass()
database = databaseClass()
rk_core = RungeKuttaClass()

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        database.db_init(self)
        self.ui.widget_2.setBackground('w')
        self.ui.widget_2.showGrid(x=True, y=True)
        self.ui.widget_3.setBackground('w')
        self.ui.widget_3.showGrid(x=True, y=True)
        self.ui.pushButton.clicked.connect(calcCore.calc_master)
        self.ui.pushButton_2.clicked.connect(self.MSG)
        self.ui.tableView.doubleClicked.connect(self.read_from_table)

    def read_from_table(self):
        for item in self.ui.tableView.selectedIndexes():
            database.selectedEngine = str(item.row() + 1)
            print(item.row() + 1)

    def MSG(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("О Программе")
        messg.setText("Разработчики:\n "
                      "Белоглазов Марк гр. 1407-240501D\n "
                      "Филимонов Иван гр. 1408-240501D")
        x = messg.exec_()
    def save_msg(self):
        messg = QtWidgets.QMessageBox()
        messg.setWindowTitle("Информация об экспорте")
        messg.setText("Данные занесены в таблицу Data.csv")
        x = messg.exec_()

app = QtWidgets.QApplication([])

application = mywindow()

application.show()
sys.exit(app.exec())