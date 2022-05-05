# main module

# import PyQt5
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi

# import local modules
import schedules, orders, drivers, vehicles


##### Root Window
class MainWindow(QMainWindow):
    def __init__(self):
        # initialize root
        super(MainWindow, self).__init__()
        self.resize(1153, 700)
        self.setMinimumSize(QSize(1153, 0))
        icon = QIcon()
        icon.addPixmap(QPixmap('icons/mainLogo.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Landscape Schedules"))
        self.CentralWidget = QWidget(self)
        self.CentralLayout = QVBoxLayout(self.CentralWidget)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.CentralLayout.setSpacing(0)
        self.setCentralWidget(self.CentralWidget)

        # initialize UI
        self.HeaderWidget = HeaderWidget(self)
        self.MainLayout = MainLayout(self)
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self, self.StackedWidget)

        # pack UI
        self.CentralLayout.addWidget(self.HeaderWidget)
        self.CentralLayout.addLayout(self.MainLayout)
        self.MainLayout.addWidget(self.IndexWidget)
        self.MainLayout.addWidget(self.StackedWidget)

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        query = QSqlQuery()
        query.exec('DELETE FROM Temp')


#### Window Header
class HeaderWidget(QWidget):
    def __init__(self, parent):
        super(HeaderWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

        loadUi('UIs/HeaderWidget.ui', self)


#### Index Widget + Stacked Widget Layout
class MainLayout(QHBoxLayout):
    def __init__(self, parent):
        super(MainLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


### Main Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent, StackedWidget):
        super(IndexWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

        loadUi('UIs/IndexWidget.ui', self)

        self.schedulesButton.clicked.connect(lambda: StackedWidget.changeIndex(0))
        self.ordersButton.clicked.connect(lambda: StackedWidget.changeIndex(1))
        self.driversButton.clicked.connect(lambda: StackedWidget.changeIndex(2))
        self.vehiclesButton.clicked.connect(lambda: StackedWidget.changeIndex(3))


### Main Working Area
class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super(StackedWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        widgets = (schedules.SchedulesWidget(), orders.OrdersWidget(), drivers.DriversWidget(),
                   vehicles.VehiclesWidget())

        for i in range(len(widgets)):
            self.addWidget(widgets[i])

    def changeIndex(self, index):
        self.setCurrentIndex(index)


##### Database Connection
def DBConnection():
    DATA = {'dbms': 'SQL Server', 'server': 'LAPTOP-32MVAP54\SQLEXPRESS', 'db': 'RRTF'}
    DETAILS = f"DRIVER={DATA['dbms']}; SERVER={DATA['server']}; DATABASE={DATA['db']}"

    connection = QSqlDatabase.addDatabase('QODBC')
    connection.setDatabaseName(DETAILS)

    if not connection.open():
        QMessageBox.critical(None, 'Error', f'Database Error: {connection.lastError().databaseText()}')
        sys.exit(1)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    DBConnection()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
