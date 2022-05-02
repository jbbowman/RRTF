# Schedules Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel

# import map libraries
from folium import Map
from io import BytesIO

##### Root Widget
class SchedulesWidget(QWidget):
    def __init__(self):
        super(SchedulesWidget, self).__init__()
        self.resize(827, 654)
        self.SchedulesLayout = QHBoxLayout(self)
        self.SchedulesLayout.setContentsMargins(0, 0, 0, 0)
        self.SchedulesLayout.setSpacing(0)

        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self, self.StackedWidget)

        self.SchedulesLayout.addWidget(self.IndexWidget)
        self.SchedulesLayout.addWidget(self.StackedWidget)


#### Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent, StackedWidget):
        super(IndexWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

        loadUi('UIs/SchedulesWidget/IndexWidget.ui', self)

        self.calendarButton.clicked.connect(lambda: StackedWidget.changeIndex(0))
        self.tableButton.clicked.connect(lambda: StackedWidget.changeIndex(1))
        self.createButton.clicked.connect(lambda: StackedWidget.changeIndex(2))


#### Main Work Area
class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super(StackedWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        widgets = (CalendarWidget(), SchedulesTable(), OrderSelectWidget())

        for i in range(len(widgets)):
            self.addWidget(widgets[i])

    def changeIndex(self, index):
        self.setCurrentIndex(index)


### Calendar
class CalendarWidget(QWidget):
    def __init__(self):
        super(CalendarWidget, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground)

        self.CalendarLayout = QVBoxLayout(self)
        self.CalendarHeaderWidget = CalendarHeaderWidget()
        self.CalendarWidget = CalendarMainWidget()

        self.CalendarLayout.addWidget(self.CalendarHeaderWidget)
        self.CalendarLayout.addWidget(self.CalendarWidget)

class CalendarHeaderWidget(QWidget):
    def __init__(self):
        super(CalendarHeaderWidget, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground)

        loadUi('UIs/SchedulesWidget/CalendarHeaderWidget.ui', self)

class CalendarMainWidget(QWidget):
    def __init__(self):
        super(CalendarMainWidget, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground)

        loadUi('UIs/SchedulesWidget/CalendarMainWidget.ui', self)


### Table
class SchedulesTable(QTableView):
    def __init__(self):
        super(SchedulesTable, self).__init__()
        self.setEditTriggers(self.DoubleClicked)
        self.setSelectionBehavior(self.SelectRows)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setSortingEnabled(True)
        self.setCornerButtonEnabled(False)
        self.horizontalHeader().setDefaultSectionSize(140)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(32)
        self.verticalHeader().setMinimumSectionSize(32)

        self.ScheduleSQL = ScheduleSQL(self)
        self.setModel(self.ScheduleSQL)

class ScheduleSQL(QSqlTableModel):
    # initialize DB Schedule table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Schedule")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        # TODO self.setHeaderData(0, Qt.Horizontal, "")
        self.select()

    # TODO sort table using bottom panel
    def sortTable(self):
        pass


### Create Order
class OrderSelectWidget(QWidget):
    def __init__(self):
        super(OrderSelectWidget, self).__init__()
        loadUi('UIs/SchedulesWidget/OrderSelectWidget.ui', self)  # load OrdersWidget XML file

        self.OrdersMap = OrdersMap(self)

        self.mapWidgetLayout.addWidget(self.OrdersMap)

class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self, parent):
        super(OrdersMap, self).__init__(parent)
        map = Map(zoom_start=9, location=(45.352281, -93.350444))
        data = BytesIO()
        map.save(data, close_file=False)
        self.setHtml(data.getvalue().decode())


if __name__ == "__main__":
    import sys, main
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main.DBConnection()
    win = SchedulesWidget()
    win.show()
    sys.exit(app.exec_())
