# Schedules Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

# import local modules
import schedulesCalendar, schedulesTable, schedulesCreate
from schedulesTable import SQL


##### Root Widget
class SchedulesWidget(QWidget):
    def __init__(self):
        super(SchedulesWidget, self).__init__()
        self.SchedulesLayout = QHBoxLayout(self)
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self)

        self.initUI()

    def initUI(self):
        self.resize(827, 654)
        self.SchedulesLayout.setContentsMargins(0, 0, 0, 0)
        self.SchedulesLayout.setSpacing(0)
        self.SchedulesLayout.addWidget(self.IndexWidget)
        self.SchedulesLayout.addWidget(self.StackedWidget)


#### Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent):
        super(IndexWidget, self).__init__(parent)
        self.parent = parent

        self.initUI()
        self.connectButtons()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/SchedulesWidget/IndexWidget.ui', self)

    def connectButtons(self):
        self.calendarButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(0))
        self.tableButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(1))
        self.createButton.clicked.connect(lambda: self.parent.StackedWidget.setCurrentIndex(2))
        self.refreshButton.clicked.connect(lambda: self.parent.StackedWidget.schedulesTable.SQL.select())
        self.refreshButton.clicked.connect(lambda: self.parent.StackedWidget.CreateWidget.SchedulesMap.setHtml(self.parent.StackedWidget.CreateWidget.SchedulesMap.createMap()))


#### Main Work Area
class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super(StackedWidget, self).__init__(parent)
        self.schedulesTable = schedulesTable.Table(self)
        self.CreateWidget = schedulesCreate.CreateWidget(self)

        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.addWidgets()

    def addWidgets(self):
        widgets = (schedulesCalendar.CalendarWidget(), self.schedulesTable, self.CreateWidget)

        for i in range(len(widgets)):
            self.addWidget(widgets[i])


if __name__ == "__main__":
    import sys, database
    from PyQt5.QtWidgets import QApplication, QMessageBox

    try:
        app = QApplication(sys.argv)
        database.DBConnection()
        win = SchedulesWidget()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
