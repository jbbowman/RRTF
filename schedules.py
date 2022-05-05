# Schedules Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel, QSqlQuery

# import map libraries
from folium import Map, Marker, MacroElement, Icon, Popup
from jinja2 import Template
from io import BytesIO
from geopy.geocoders import Nominatim


##### Root Widget
class SchedulesWidget(QWidget):
    def __init__(self):
        super(SchedulesWidget, self).__init__()
        self.resize(827, 654)
        self.SchedulesLayout = QHBoxLayout(self)
        self.SchedulesLayout.setContentsMargins(0, 0, 0, 0)
        self.SchedulesLayout.setSpacing(0)

        # initialize UI
        self.StackedWidget = StackedWidget(self)
        self.IndexWidget = IndexWidget(self, self.StackedWidget)

        # pack UI
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

        widgets = (CalendarWidget(), SchedulesTable(), CreateWidget())

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
class CreateWidget(QWidget):
    def __init__(self):
        super(CreateWidget, self).__init__()
        loadUi('UIs/SchedulesWidget/CreateWidget.ui', self)  # load OrdersWidget XML file

        self.OrdersMap = OrdersMap(self)
        self.TempSQL = TempSQL(self.selectedTable)

        self.selectedTable.setModel(self.TempSQL)
        self.MapLayout.addWidget(self.OrdersMap)

        self.submitButton.clicked.connect(lambda: self.createSchedule())

    def createSchedule(self):
        driverID = self.getValue(f"SELECT driverID FROM Driver WHERE lastName = '{self.driverSearch.currentText()}'")
        vehicleID = self.getValue(f"SELECT vehicleID FROM Vehicle WHERE name = '{self.vehicleSearch.currentText()}'")
        date = self.dateEdit.date().toString('yyyyddMM')
        stops = self.getValue('SELECT COUNT(invoiceID) FROM Temp;')
        items = self.getValue('SELECT COUNT(invoiceID) FROM OrderItem WHERE invoiceID IN (SELECT invoiceID FROM Temp);')
        workHours = self.getValue('SELECT SUM(workHours) FROM Temp;')
        driveHours = 999999
        notes = 'N/A'

        query = QSqlQuery()
        print(driverID, vehicleID, date, stops, items, workHours, driveHours, notes)
        if query.exec(f"INSERT INTO Schedule VALUES ({driverID}, {vehicleID}, '{date}', {stops}, {items}, {workHours}, {driveHours}, '{notes}');"):
            query.exec('UPDATE Orders SET scheduleID = SCOPE_IDENTITY() WHERE invoiceID IN (SELECT invoiceID FROM Temp)')
            query.exec(f"UPDATE Orders SET deliveryDate = '{date}' WHERE invoiceID IN (SELECT invoiceID FROM Temp)")
            query.exec('DELETE FROM Temp')
            self.TempSQL.select()

    def getValue(self, statement):
        query = QSqlQuery()
        query.exec(statement)
        query.next()
        return query.value(0)

class TempSQL(QSqlTableModel):
    # initialize DB Schedule table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Temp")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)

        columns = ['Invoice ID', 'Schedule ID', 'Delivery Date', 'Work Hours', 'First Name', 'Last Name', 'Street',
                   'City', 'State', 'Zip Code', 'Phone', 'Order Date', 'Description']

        for i in range(len(columns)):
            self.setHeaderData(i, Qt.Horizontal, columns[i])

class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self, parent):
        super(OrdersMap, self).__init__(parent)
        self.parent = parent
        foliumMap = Map(location=(45.352281, -93.350444), zoom_start=9)
        self.addMarkerEventListener()
        self.addMarkers(foliumMap)
        self.getMarkerPopupContents(foliumMap)
        data = BytesIO()
        foliumMap.save(data, close_file=False)
        page = WebEnginePage(self)
        self.setPage(page)
        self.setHtml(data.getvalue().decode())  # give html of folium map to webengine

    def addMarkerEventListener(self): #make event listener for markers
        file = open('maptools/addmarkereventlistener.js', 'r')
        data = file.read()
        Marker._mytemplate = Template(data)

        def myMarkerInit(self, *args, **kwargs):
            self.__initOriginal__(*args, **kwargs)
            self._template = self._mytemplate

        Marker.__initOriginal__ = Marker.__init__
        Marker.__init__ = myMarkerInit

    def addMarkers(self, mapObject):
        locator = Nominatim(user_agent='LandscapeScheduling')
        query = QSqlQuery()
        query.exec('SELECT * FROM Orders;')

        while query.next():
            popup = Popup(f'Invoice ID: {query.value(0)} <br>'
                          f'Work Hours: {query.value(3)} <br>'
                          f'Order Date: {query.value(11)} <br>'
                          f'Name: {query.value(4)} {query.value(5)} <br>'
                          f'Phone Number: {query.value(10)} <br>'
                          f'Address: {query.value(6)}, {query.value(7)}, {query.value(8)} {query.value(9)}',
                          min_width=200, max_width=200)
            location = locator.geocode(f'{query.value(6)}, {query.value(7)}, {query.value(8)} {query.value(9)}')
            Marker(location=(location.latitude, location.longitude),
                   icon=Icon(color='darkgreen', icon='map-marker'),
                   popup=popup).add_to(mapObject)

    def getMarkerPopupContents(self, mapObject):
        file = open('maptools/getmarkercontents.js', 'r')
        data = file.read()
        el = MacroElement().add_to(mapObject)
        el._template = Template(data)

    def handleConsoleMessage(self, msg):
        invoiceID = int(msg.split()[2])
        query = QSqlQuery()
        query.exec('SELECT * FROM Temp;')
        temp = []

        while query.next():
            temp.append(query.value(0))

        if invoiceID not in temp:
            query.exec(f'INSERT INTO Temp SELECT * FROM Orders WHERE invoiceID = {invoiceID};')

        elif invoiceID in temp:
            query.exec(f'DELETE FROM Temp WHERE invoiceID = {invoiceID}')

        self.parent.TempSQL.select()

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if 'Invoice ID' in msg:
            self.parent.handleConsoleMessage(msg)


if __name__ == "__main__":
    import sys, main
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main.DBConnection()
    win = SchedulesWidget()
    win.show()
    sys.exit(app.exec_())
