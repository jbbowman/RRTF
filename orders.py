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

        self.OrdersMap = OrdersMap(self)
        self.OrdersSQL = OrdersSQL(self)

        self.mapWidgetLayout.addWidget(self.OrdersMap)
        self.ordersTable.setModel(self.OrdersSQL)


class OrdersMap(QWebEngineView):
    # initialize orders map
    def __init__(self, parent):
        super(OrdersMap, self).__init__(parent)
        map = Map(zoom_start=9, location=(45.352281, -93.350444))
        data = BytesIO()
        map.save(data, close_file=False)
        self.setHtml(data.getvalue().decode())


class OrdersSQL(QSqlTableModel):
    # initialize DB Orders table CONNECTION
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
    main.DBConnection()
    win = OrdersWidget()
    win.show()
    sys.exit(app.exec_())
