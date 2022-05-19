# Vehicles Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel

# import local modules
import map


##### Root Widget
class VehiclesWidget(QWidget):
    def __init__(self):
        super(VehiclesWidget, self).__init__()
        self.VehiclesLayout = QHBoxLayout(self)

        self.VehiclesTable = VehiclesTable(self)
        self.IndexWidget = IndexWidget(self)

        self.initUI()

    def initUI(self):
        self.resize(827, 654)
        self.VehiclesLayout.setContentsMargins(0, 0, 0, 0)
        self.VehiclesLayout.setSpacing(0)
        self.VehiclesLayout.addWidget(self.IndexWidget)
        self.VehiclesLayout.addLayout(self.VehiclesTable)



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
        self.createButton.clicked.connect(self.parent.VehiclesTable.addRow)
        self.deleteButton.clicked.connect(self.parent.VehiclesTable.delRow)


class VehiclesTable(QVBoxLayout):
    def __init__(self, parent):
        super(VehiclesTable, self).__init__(parent)
        self.model = QSqlTableModel()
        self.view = QTableView()

        self.initUI()

    def initUI(self):
        self.model.setTable("Vehicle")
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
        columns = ['Vehicle ID', 'Name', 'Class', 'Vehicle Wt Cap', 'Trailer Wt Cap', 'Surface Area', 'Active?', 'Notes']

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
    win = VehiclesWidget()
    win.show()
    sys.exit(app.exec_())
