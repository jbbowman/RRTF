# Orders Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWebEngineWidgets import QWebEngineView

# import Map/IO
from folium import Map
from io import BytesIO


class OrdersWidget(QWidget):
    # initialize orders widget
    def __init__(self):
        super(OrdersWidget, self).__init__()
        loadUi('UIs/OrdersWidget.ui', self)  # load OrdersWidget XML file

        self.initOrdersMap()
        self.initOrdersTable()
        self.initSelectedTable()

    # attach orders map to orders widget
    def initOrdersMap(self):
        self.OrdersMap = OrdersMap(9, (45.352281, -93.350444))
        data = BytesIO()
        self.OrdersMap.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.mapWidgetLayout.addWidget(webView)

    # attach orders table to orders widget
    def initOrdersTable(self):
        self.OrdersSQL = OrdersSQL(self)
        self.ordersTable.setModel(self.OrdersSQL)

    # TODO attach selected orders table to orders widget
    def initSelectedTable(self):
        pass

class OrdersMap(Map):
    # initialize orders map
    def __init__(self, zoom_start, location):
        super(OrdersMap, self).__init__(zoom_start=zoom_start, location=location)


class OrdersSQL(QSqlTableModel):
    # initialize DB Orders table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Orders")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        # TODO self.setHeaderData(0, Qt.Horizontal, "")
        self.select()

    # TODO sort table using bottom panel
    def sortTable(self):
        pass


if __name__ == "__main__":
    import sys
    import main
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    if not main.connectDB():
        sys.exit(1)
    win = OrdersWidget()
    win.show()
    sys.exit(app.exec_())
