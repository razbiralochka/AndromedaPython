import sys
from PyQt5 import QtWidgets, QtSql
from myform import Ui_MainWindow

# import pyqtgraph as pg
# from pyqtgraph import PlotWidget

from Database import Database
from Calculation import calculations


DBFILENAME = './engine.mdb'


class MainWindow(QtWidgets.QMainWindow):
    calcCore = None
    db = None
    __model = None

    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.launch_calc)
        self.ui.pushButton_2.clicked.connect(self.show_about)

    def associate_calc_core(self, calc_func):
        self.calcCore = calc_func

    def associate_catabase(self, db):
        self.__model = QtSql.QSqlTableModel(self, db.get_db())
        self.__model.setTable("engine")
        self.__model.select()

        self.ui.tableView.setModel(self.__model)
        self.ui.tableView.doubleClicked.connect(self.read_from_table)

    def read_from_table(self):
        for item in self.ui.tableView.selectedIndexes():
            # self.selectedEngine = str(item.row() + 1)

            print(self.ui.tableView.model().index(item.row(), 1).data())
            print(self.ui.tableView.model().index(item.row(), 2).data())
            print(self.ui.tableView.model().index(item.row(), 3).data())
            print(self.ui.tableView.model().index(item.row(), 4).data())
            print(self.ui.tableView.model().index(item.row(), 5).data())
            print(self.ui.tableView.model().index(item.row(), 6).data())

            self.ui.lineEdit_16.setText(str(self.ui.tableView.model().index(item.row(), 2).data()))
            buf = float(self.ui.tableView.model().index(item.row(), 3).data())*1000
            self.ui.lineEdit_8.setText(str(buf))
            self.ui.lineEdit_17.setText(str(self.ui.tableView.model().index(item.row(), 4).data()))
            self.ui.lineEdit_3.setText(str(self.ui.tableView.model().index(item.row(), 5).data()))
            self.ui.lineEdit_23.setText(self.ui.tableView.model().index(item.row(), 1).data())

    @staticmethod
    def show_about():
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("О Программе")
        msg.setText("Хайруллин И.И.")
        msg.exec_()

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
    app = QtWidgets.QApplication([])

    database = Database()
    if not database.connect(DBFILENAME):
        print('error db open' + str(database.get_last_error()))
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка открытия Базы Данных")
        msg.setText(str(database.get_last_error()))
        msg.exec_()

    calc_core = calculations()

    application = MainWindow()
    if database.getdbstate():
        application.associate_catabase(database)

    application.associate_calc_core(calc_core)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
