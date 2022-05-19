# Orders Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel

# import local modules
import map


##### Root Widget
class OrdersWidget(QWidget):
    def __init__(self):
        super(OrdersWidget, self).__init__()
        self.OrdersLayout = QHBoxLayout(self)

        self.OrdersMap = map.OrdersMap(self)
        self.OrdersTable = OrdersTable(self)

        self.IndexWidget = IndexWidget(self)
        self.MapTableLayout = QVBoxLayout(self)

        self.initUI()

    def initUI(self):
        self.resize(827, 654)
        self.OrdersLayout.setContentsMargins(0, 0, 0, 0)
        self.OrdersLayout.setSpacing(0)
        self.OrdersLayout.addWidget(self.IndexWidget)
        self.OrdersLayout.addLayout(self.MapTableLayout)
        self.OrdersMap.setHtml(self.OrdersMap.createMap())
        self.MapTableLayout.addWidget(self.OrdersMap)
        self.MapTableLayout.addLayout(self.OrdersTable)
        self.MapTableLayout.setStretch(0, 1)
        self.MapTableLayout.setStretch(1, 1)



#### Selection Menu
class IndexWidget(QWidget):
    def __init__(self, parent):
        super(IndexWidget, self).__init__(parent)
        self.parent = parent

        self.initUI()
        self.connectButtons()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground)
        loadUi('UIs/OrdersWidget/IndexWidget.ui', self)

    def connectButtons(self):
        self.createButton.clicked.connect(self.parent.OrdersTable.addRow)
        self.deleteButton.clicked.connect(self.parent.OrdersTable.delRow)
        self.refreshButton.clicked.connect(self.parent.OrdersTable.model.select)
        self.refreshButton.clicked.connect(lambda: self.parent.OrdersMap.setHtml(self.parent.OrdersMap.createMap()))


class OrdersTable(QVBoxLayout):
    def __init__(self, parent):
        super(OrdersTable, self).__init__(parent)
        self.model = QSqlTableModel()
        self.view = QTableView()

        self.initUI()

    def initUI(self):
        self.model.setTable("Orders")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.setColumns()
        self.model.select()

        self.view.setModel(self.model)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.view.setEditTriggers(self.view.DoubleClicked)
        self.view.setSelectionBehavior(self.view.SelectRows)
        self.view.setVerticalScrollMode(self.view.ScrollPerPixel)
        self.view.setHorizontalScrollMode(self.view.ScrollPerPixel)
        self.view.setSortingEnabled(True)
        self.view.setCornerButtonEnabled(False)
        self.view.horizontalHeader().setDefaultSectionSize(140)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(32)
        self.view.verticalHeader().setMinimumSectionSize(32)
        self.view.clicked.connect(self.findRow)

        self.addWidget(self.view)


    def setColumns(self):
        columns = ['Invoice ID', 'Schedule ID', 'Delivery Date', 'Work Hours', 'Drive Hours', 'First Name', 'Last Name',
                   'Street Address', 'City', 'State', 'Zip Code', 'Phone', 'Order Date', 'Description']

        for i in range(len(columns)):
            self.model.setHeaderData(i, Qt.Horizontal, columns[i])

    def findRow(self, i):
        deleterow = i.row()

    def addRow(self):
        ret = self.model.insertRows(self.model.rowCount(), 1)

    def delRow(self):
        self.view.setRowHidden(self.view.currentIndex().row(), True)
        self.model.removeRow(self.view.currentIndex().row())

if __name__ == "__main__":
    import sys, database
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    database.DBConnection()
    win = OrdersWidget()
    win.show()
    sys.exit(app.exec_())
