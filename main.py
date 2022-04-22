# main module

# import PyQt5
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtSql import QSqlDatabase
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore

# import local modules
import schedules, orders, drivers, vehicles, settings, about


class MainWindow(QMainWindow):  # define root
    # initialize root
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1153, 700)
        self.setMinimumSize(QtCore.QSize(1153, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/mainLogo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "Schedule Creator"))
        QtCore.QMetaObject.connectSlotsByName(self)

        self.initUI()

    # initialize UI components
    def initUI(self):
        # initiate central widget and attach it to root
        self.CentralWidget = CentralWidget(self)
        self.centralLayout = self.CentralWidget.centralLayout
        self.setCentralWidget(self.CentralWidget)

        # initiate widgets
        self.WorkspaceWidget = WorkspaceWidget(self)
        self.workspaceLayout = self.WorkspaceWidget.workspaceLayout
        self.TopPanelWidget = TopPanelWidget(self, schedules.SchedulesWidget)
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self, self.StackedWidget, self.TopPanelWidget)

        # attach widgets to central widget
        self.centralLayout.addWidget(self.IndexWidget)
        self.centralLayout.addWidget(self.WorkspaceWidget)
        self.workspaceLayout.addWidget(self.TopPanelWidget)
        self.workspaceLayout.addWidget(self.StackedWidget)


class CentralWidget(QWidget):  # define central widget
    # initialize central widget and layout to attach all UI components
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

        # central layout
        self.centralLayout = QHBoxLayout(self)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.setSpacing(0)


class IndexWidget(QWidget):  # define index widget
    # initialize index widget to navigate stacked widget
    def __init__(self, parent, StackedWidget, TopPanelWidget):
        super(IndexWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(135, 135, 135);")

        # load IndexWidget UI
        loadUi('UIs/IndexWidget.ui', self)

        # connect buttons to respective stacked widget index
        self.schedulesButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 0, 'Schedules'))
        self.ordersButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 1, 'Orders'))
        self.driversButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 2, 'Drivers'))
        self.vehiclesButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 3, 'Vehicles'))
        self.settingsButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 4, 'Settings'))
        self.aboutButton.clicked.connect(lambda: self.changeIndex(StackedWidget, TopPanelWidget, 5, 'About'))

    # change stacked widget index
    def changeIndex(self, StackedWidget, TopPanelWidget, index, string):
        StackedWidget.setCurrentIndex(index)
        TopPanelWidget.mainLabel.setText(string)


class WorkspaceWidget(QWidget):  # define workspace widget
    # initialize workspace widget and layout to attach top panel widget and stacked widget
    def __init__(self, parent):
        super(WorkspaceWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(180, 180, 180);")

        # work space layout
        self.workspaceLayout = QVBoxLayout(self)
        self.workspaceLayout.setContentsMargins(0, 0, 0, 0)
        self.workspaceLayout.setSpacing(0)


class TopPanelWidget(QWidget):  # define top panel widget
    # initialize top panel widget to label workspace and add buttons
    def __init__(self, parent, DBtable):
        super(TopPanelWidget, self).__init__(parent)
        loadUi('UIs/TopPanelWidget.ui', self)  # load TopPanel XML file

        self.createButton.clicked.connect(lambda: self.addRow(DBtable))

    # TODO add row to respective table
    def addRow(self, DBtable):  # parameters = currentIndex
        print(DBtable.rowCount())
        DBtable.insertRows(DBtable.rowCount(), 1)

    # TODO delete row from respective table
    def delRow(self, DBtable):  # parameters = currentIndex
        pass


class StackedWidget(QStackedWidget):  # define stacked widget
    # initialize stacked widget to dynamically change widgets in root window
    def __init__(self, parent):
        super(QStackedWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(180, 180, 180);")

        # add widgets to stacked widget
        self.addWidget(schedules.SchedulesWidget())  # Index 0
        self.addWidget(orders.OrdersWidget())  # Index 1
        self.addWidget(drivers.DriversWidget())  # Index 2
        self.addWidget(vehicles.VehiclesWidget())  # Index 3
        self.addWidget(settings.SettingsWidget())  # Index 4
        self.addWidget(about.AboutWidget())  # Index 5


def connectDB():  # connect RRTF database
    DBMS_NAME = 'SQL Server'
    SERVER_NAME = 'LAPTOP-32MVAP54\SQLEXPRESS'
    DB_NAME = 'RRTF'
    DB_DETAILS = f'DRIVER={DBMS_NAME}; SERVER={SERVER_NAME}; DATABASE={DB_NAME}'

    connection = QSqlDatabase.addDatabase('QODBC')
    connection.setDatabaseName(DB_DETAILS)

    # if database not found, error message displays
    if not connection.open():
        QMessageBox.critical(None, 'Error', f'Database Error: {connection.lastError().databaseText()}')
        return False
    return True


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    if not connectDB():
        sys.exit(1)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
