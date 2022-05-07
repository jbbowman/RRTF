# main module

# import PyQt5
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi

# import local modules
import schedules, orders, drivers, vehicles, database as db


##### Root Window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.CentralWidget = QWidget(self)
        self.CentralLayout = QVBoxLayout(self.CentralWidget)
        self.HeaderWidget = HeaderWidget(self)
        self.MainLayout = MainLayout(self)
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self)

        self.initUI()

    def initUI(self):
        self.resize(1153, 700)
        self.setMinimumSize(QSize(1153, 0))
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Landscape Schedules"))
        self.addIcon()
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.CentralLayout.setSpacing(0)
        self.setCentralWidget(self.CentralWidget)
        self.CentralLayout.addWidget(self.HeaderWidget)
        self.CentralLayout.addLayout(self.MainLayout)
        self.MainLayout.addWidget(self.IndexWidget)
        self.MainLayout.addWidget(self.StackedWidget)
        
    def addIcon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap('icons/mainLogo.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        db.query.exec('DELETE FROM Temp;')


#### Window Header
class HeaderWidget(QWidget):
    def __init__(self, parent):
        super(HeaderWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/HeaderWidget.ui', self)


#### Index Widget + Stacked Widget Layout
class MainLayout(QHBoxLayout):
    def __init__(self, parent):
        super(MainLayout, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


### Main Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent):
        super(IndexWidget, self).__init__(parent)
        self.parent = parent

        self.initUI()
        self.connectButtons()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/IndexWidget.ui', self)

    def connectButtons(self):
        self.schedulesButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(0))
        self.ordersButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(1))
        self.driversButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(2))
        self.vehiclesButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(3))


### Main Working Area
class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super(StackedWidget, self).__init__(parent)
        self.initUI()
        self.addWidgets()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

    def addWidgets(self):
        widgets = (schedules.SchedulesWidget(), orders.OrdersWidget(), drivers.DriversWidget(),
                   vehicles.VehiclesWidget())

        for i in range(len(widgets)):
            self.addWidget(widgets[i])


if __name__ == "__main__":
    import sys, database
    from PyQt5.QtWidgets import QApplication, QMessageBox

    try:
        app = QApplication(sys.argv)
        database.DBConnection()
        win = MainWindow()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
