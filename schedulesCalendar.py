# import PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class CalendarWidget(QWidget):
    def __init__(self):
        super(CalendarWidget, self).__init__()
        self.CalendarLayout = QVBoxLayout(self)
        self.CalendarHeaderWidget = CalendarHeaderWidget()
        self.CalendarWidget = CalendarMainWidget()

        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.CalendarLayout.addWidget(self.CalendarHeaderWidget)
        self.CalendarLayout.addWidget(self.CalendarWidget)


class CalendarHeaderWidget(QWidget):
    def __init__(self):
        super(CalendarHeaderWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/SchedulesWidget/CalendarHeaderWidget.ui', self)


class CalendarMainWidget(QWidget):
    def __init__(self):
        super(CalendarMainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/SchedulesWidget/CalendarMainWidget.ui', self)


if __name__ == "__main__":
    import sys, database
    from PyQt5.QtWidgets import QApplication, QMessageBox

    try:
        app = QApplication(sys.argv)
        database.DBConnection()
        win = CalendarWidget()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred {exception}')
        sys.exit(1)
