from jinja2 import Template
from folium import Map, Marker, MacroElement
from io import BytesIO

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class CreateWidget(QWidget):
    def __init__(self):
        super(CreateWidget, self).__init__()
        loadUi('UIs/SchedulesWidget/CreateWidget.ui', self)  # load OrdersWidget XML file

        self.OrdersMap = OrdersMap(self)
        self.MapLayout.addWidget(self.OrdersMap)

class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self, parent):
        super(OrdersMap, self).__init__(parent)
        self.foliumMap = Map(location=[45.5236, -122.6750], zoom_start=13)
        markers = [[45.5012, -122.6655], [45.5132, -122.6708], [45.5275, -122.6692], [45.5318, -122.6745]]

        self.addPopups()
        self.addMarkers(self.foliumMap, markers)
        self.addJS(self.foliumMap)

        data = BytesIO()
        self.foliumMap.save(data, close_file=False)

        page = WebEnginePage(self)
        self.setPage(page)
        self.setHtml(data.getvalue().decode())  # give html of folium map to webengine

    def addPopups(self):
        tmpldata = """<!-- monkey patched Marker template -->
                    {% macro script(this, kwargs) %}
                        var {{ this.get_name() }} = L.marker(
                            {{ this.location|tojson }},
                            {{ this.options|tojson }}
                        ).addTo({{ this._parent.get_name() }}).on('click', onClick);
                    {% endmacro %}
                    """

        Marker._mytemplate = Template(tmpldata)

        def myMarkerInit(self, *args, **kwargs):
            self.__initOriginal__(*args, **kwargs)
            self._template = self._mytemplate

        Marker.__initOriginal__ = Marker.__init__
        Marker.__init__ = myMarkerInit

    def addMarkers(self, mapObject, markerLocations):
        for location in markerLocations:  # range(locations.shape[0]):
            Marker(location=location, popup=f'<p id="latlon">{location[0]}, {location[1]}</p>').add_to(mapObject)

    def addJS(self, mapObject):
        el = MacroElement().add_to(mapObject)
        el._template = Template("""
                {% macro script(this, kwargs) %}
                function getInnerText( sel ) {
                    var txt = '';
                    $( sel ).contents().each(function() {
                        var children = $(this).children();
                        txt += ' ' + this.nodeType === 3 ? this.nodeValue : children.length ? getInnerText( this ) : $(this).text();
                    });
                    return txt;
                };

                function onClick(e) {
                   var popup = e.target.getPopup();
                   var content = popup.getContent();
                   text = getInnerText(content);
                   console.log(text);
                };
                {% endmacro %}
            """)

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        print(msg) # Check js errors
        if 'coordinates' in msg:
            self.parent.handleConsoleMessage(msg)


if __name__ == "__main__":
    import sys, main
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main.DBConnection()
    win = CreateWidget()
    win.show()
    sys.exit(app.exec_())