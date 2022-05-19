# import PyQt5
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox

# import map libraries
from folium import Marker, MacroElement, Icon, Popup
from jinja2 import Template
from geopy.geocoders import Nominatim
from openrouteservice import Client
from folium import Map
from io import BytesIO

# import local modules
import database as db


class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self, parent):
        super(OrdersMap, self).__init__(parent)

    def createMap(self):
        try:
            foliumMap = Map(location=(45.352281, -93.350444), zoom_start=9)
            data = BytesIO()
            self.getMarkerPopup(foliumMap)
            self.addMarkers(foliumMap)
            foliumMap.save(data, close_file=False)
            return data.getvalue().decode()
        except Exception as exception:
            QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')

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
        tempTable = db.getTable1('SELECT invoiceID FROM Temp;')
        db.query.exec('SELECT * FROM Orders WHERE scheduleID IS NULL;')

        while db.query.next():
            invoiceID = db.query.value(0)
            popup = Popup(f'Invoice ID: {invoiceID} <br>'
                          f'Work Hours: {db.query.value(3)} <br>'
                          f'Order Date: {db.query.value(12)} <br>'
                          f'Name: {db.query.value(5)} {db.query.value(6)} <br>'
                          f'Phone Number: {db.query.value(11)} <br>'
                          f'Address: {db.query.value(7)}, {db.query.value(8)}, {db.query.value(9)} {db.query.value(10)}',
                          min_width=200, max_width=200)

            location = getCoords(db.query.value(7), db.query.value(8), db.query.value(9), db.query.value(10), False)

            if invoiceID not in tempTable:
                Marker(location=location,
                       icon=Icon(color='darkgreen', icon='map-marker'),
                       popup=popup).add_to(mapObject)
            else:
                Marker(location=location,
                       icon=Icon(color='red', icon='map-marker'),
                       popup=popup).add_to(mapObject)

    def getMarkerPopup(self, mapObject):
        file = open('maptools/getmarkercontents.js', 'r')
        data = file.read()
        el = MacroElement().add_to(mapObject)
        el._template = Template(data)


def getCoords(street, city, state, zipCode, longFirst=True):
    client = Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
    address = f'{street}, {city}, {state} {zipCode}'
    res = client.pelias_search(text=address)

    if longFirst:
        return res['features'][0]['geometry']['coordinates'][0], res['features'][0]['geometry']['coordinates'][1]
    else:
        return res['features'][0]['geometry']['coordinates'][1], res['features'][0]['geometry']['coordinates'][0]


def getDriveTime(location1, location2):
    client = Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
    coords = (location1, location2)
    res = client.directions(coords)
    return round(res['routes'][0]['summary']['duration'] / 3600, 2)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    try:
        app = QApplication(sys.argv)
        db.DBConnection()
        win = OrdersMap()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
