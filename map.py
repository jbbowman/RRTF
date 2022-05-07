# import PyQt5
from PyQt5.QtWebEngineWidgets import QWebEngineView

# import map libraries
from folium import Marker, MacroElement, Icon, Popup
from jinja2 import Template
from geopy.geocoders import Nominatim
from openrouteservice import Client

# import local modules
import database as db


class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self):
        super(OrdersMap, self).__init__()
        self.addMarkerEventListener()

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
        db.query.exec('SELECT * FROM Orders WHERE scheduleID IS NULL;')

        while db.query.next():
            popup = Popup(f'Invoice ID: {db.query.value(0)} <br>'
                          f'Work Hours: {db.query.value(3)} <br>'
                          f'Order Date: {db.query.value(12)} <br>'
                          f'Name: {db.query.value(5)} {db.query.value(6)} <br>'
                          f'Phone Number: {db.query.value(11)} <br>'
                          f'Address: {db.query.value(7)}, {db.query.value(8)}, {db.query.value(9)} {db.query.value(10)}',
                          min_width=200, max_width=200)

            location = getCoords(db.query.value(7), db.query.value(8), db.query.value(9), db.query.value(10), False)
            Marker(location=location,
                   icon=Icon(color='darkgreen', icon='map-marker'),
                   popup=popup).add_to(mapObject)

    def getMarkerPopup(self, mapObject):
        file = open('maptools/getmarkercontents.js', 'r')
        data = file.read()
        el = MacroElement().add_to(mapObject)
        el._template = Template(data)


def getCoords(street, city, state, zipCode, longFirst=True):
    locator = Nominatim(user_agent='LandscapeScheduling')
    location = locator.geocode(f'{street}, {city}, {state} {zipCode}')

    if longFirst:
        return location.longitude, location.latitude
    else:
        return location.latitude, location.longitude


def getDriveTime(location1, location2):
    client = Client(key='5b3ce3597851110001cf6248306ecbc8079946f483cba81d17c4144a')
    coords = (location1, location2)
    res = client.directions(coords)
    return round(res['routes'][0]['summary']['duration'] / 3600, 2)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMessageBox

    try:
        app = QApplication(sys.argv)
        db.DBConnection()
        win = OrdersMap()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
