# import PyQt5
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel

# import folium/io
from folium import Map
from io import BytesIO

# import local modules
import map, database as db


class CreateWidget(QWidget):
    def __init__(self):
        super(CreateWidget, self).__init__()
        self.SchedulesMap = SchedulesMap(self)
        self.initUI()
        self.connectButtons()

    def initUI(self):
        loadUi('UIs/SchedulesWidget/CreateWidget.ui', self)  # load OrdersWidget XML file
        self.TempSQL = TempSQL(self.selectedTable)
        self.selectedTable.setModel(self.TempSQL)
        self.dateEdit.setDate(QDate.currentDate())

        self.MapLayout.addWidget(self.SchedulesMap)

    def connectButtons(self):
        self.submitButton.clicked.connect(lambda: self.createSchedule())

    def createSchedule(self):
        # add schedule to table
        if db.getValue('SELECT COUNT(*) FROM Temp;') != 0:
            driverID = db.getValue(f"SELECT driverID FROM Driver WHERE lastName = '{self.driverSearch.currentText()}';")
            vehicleID = db.getValue(f"SELECT vehicleID FROM Vehicle WHERE name = '{self.vehicleSearch.currentText()}';")
            date = self.dateEdit.date().toString('yyyyddMM')
            stops = db.getValue('SELECT COUNT(invoiceID) FROM Temp;')
            items = self.scheduleItems.value()
            loadHours = 1.0
            workHours = db.getValue('SELECT SUM(workHours) FROM Temp;')
            driveHours = self.driverHrsCount.value()
            notes = 'N/A'

            # submit schedule, reset selection table
            if db.query.exec(f"INSERT INTO Schedule VALUES ({driverID}, {vehicleID}, '{date}', {stops}, {items}, "
                             f"{loadHours}, {workHours}, {driveHours}, '{notes}');"):

                db.query.exec('UPDATE Orders SET scheduleID = SCOPE_IDENTITY() WHERE invoiceID IN (SELECT invoiceID '
                              'FROM Temp);')

                db.query.exec(f"UPDATE Orders SET deliveryDate = '{date}' WHERE invoiceID IN (SELECT invoiceID FROM "
                              f"Temp);")

                db.query.exec('UPDATE Orders SET Orders.driveHours = Temp.driveHours FROM Orders INNER JOIN Temp ON '
                              'Orders.invoiceID = Temp.invoiceID;')

                db.query.exec('DELETE FROM Temp;')

                self.TempSQL.select()
                self.scheduleItems.setValue(0)
                self.driverHrsCount.setValue(0)

            self.SchedulesMap.setHtml(self.SchedulesMap.createMap())

        else:
            QMessageBox.critical(None, 'Error', f'No order selections have been made')


class SchedulesMap(map.OrdersMap):
    def __init__(self, parent):
        super(SchedulesMap, self).__init__()
        self.parent = parent
        self.addPage()
        self.setHtml(self.createMap())

    def createMap(self):
        foliumMap = Map(location=(45.352281, -93.350444), zoom_start=9)
        data = BytesIO()
        self.getMarkerPopup(foliumMap)
        self.addMarkers(foliumMap)
        foliumMap.save(data, close_file=False)
        return data.getvalue().decode()

    def addScheduleOrder(self, invoiceID):
        count = db.getValue('SELECT COUNT(invoiceID) FROM Temp;')
        exists = db.getValue(f'SELECT COUNT(invoiceID) FROM Temp WHERE invoiceID = {invoiceID};')

        if not exists:  # add order to selection table
            db.query.exec(f'INSERT INTO Temp SELECT invoiceID, orderDate, workHours, driveHours, firstName, lastName, '
                          f'phone, streetAddress, city, state, zipCode FROM Orders WHERE invoiceID = {invoiceID};')

            tableStack = db.getTableStack('SELECT streetAddress, city, state, zipCode FROM Temp;', 4, 2)
            l1 = map.getCoords(tableStack[0][0], tableStack[0][1], tableStack[0][2], tableStack[0][3])

            if count == 0:  # add distance from company
                l2 = map.getCoords('21050 Lake George Blvd', 'Oak Grove', 'MN', 55303)

            else:  # add distance from previous order location
                l2 = map.getCoords(tableStack[1][0], tableStack[1][1], tableStack[1][2], tableStack[1][3])

            driveTime = map.getDriveTime(l1, l2)
            db.query.exec(f'UPDATE Temp SET driveHours = {driveTime} WHERE invoiceID = {invoiceID};')

        else:  # remove order from selection table
            db.query.exec(f'DELETE FROM Temp WHERE invoiceID = {invoiceID};')

        self.parent.driverHrsCount.setValue(db.getValue('SELECT SUM(driveHours) FROM Temp;'))
        self.parent.scheduleItems.setValue(db.getValue('SELECT COUNT(invoiceID) FROM OrderItem WHERE invoiceID IN '
                                                       '(SELECT invoiceID FROM Temp);'))
        self.parent.TempSQL.select()

    def addPage(self):
        page = WebEnginePage(self)
        self.setPage(page)


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        if 'Invoice ID' in msg:
            invoiceID = int(msg.split()[2])
            self.parent.addScheduleOrder(invoiceID)


class TempSQL(QSqlTableModel):
    def __init__(self, parent):
        super(TempSQL, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTable("Temp")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.setColumns()

    def setColumns(self):
        columns = ['Invoice ID', 'Order Date', 'Work Hours', 'Drive Hours', 'First Name', 'Last Name', 'Phone',
                   'Street', 'City', 'State', 'Zip Code']

        for i in range(len(columns)):
            self.setHeaderData(i, Qt.Horizontal, columns[i])


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    try:
        app = QApplication(sys.argv)
        db.DBConnection()
        win = CreateWidget()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
