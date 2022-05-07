# Schedules Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

# import local modules
import schedulesCalendar, schedulesTable, schedulesCreate


##### Root Widget
class SchedulesWidget(QWidget):
    def __init__(self):
        super(SchedulesWidget, self).__init__()
        self.SchedulesLayout = QHBoxLayout(self)
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self, self.StackedWidget)

        self.initUI()

    def initUI(self):
        self.resize(827, 654)
        self.SchedulesLayout.setContentsMargins(0, 0, 0, 0)
        self.SchedulesLayout.setSpacing(0)
        self.SchedulesLayout.addWidget(self.IndexWidget)
        self.SchedulesLayout.addWidget(self.StackedWidget)


#### Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent, StackedWidget):
        super(IndexWidget, self).__init__(parent)
        self.initUI()
        self.connectButtons(StackedWidget)

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/SchedulesWidget/IndexWidget.ui', self)

    def connectButtons(self, StackedWidget):
        self.calendarButton.clicked.connect(lambda: StackedWidget.setCurrentIndex(0))
        self.tableButton.clicked.connect(lambda: StackedWidget.setCurrentIndex(1))
        self.createButton.clicked.connect(lambda: StackedWidget.setCurrentIndex(2))


#### Main Work Area
class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super(StackedWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.addWidgets()

    def addWidgets(self):
        widgets = (schedulesCalendar.CalendarWidget(), schedulesTable.Table(), schedulesCreate.CreateWidget())

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
