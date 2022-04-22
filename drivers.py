# Drivers Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel


class DriversWidget(QWidget):
    # initialize drivers widget
    def __init__(self):
        super(DriversWidget, self).__init__()
        loadUi('UIs/DriversWidget.ui', self)  # load DriversWidget XML file

        self.initDriversTable()

    # attach drivers table to drivers widget
    def initDriversTable(self):
        self.DriverSQL = DriverSQL(self)
        self.driversTable.setModel(self.DriverSQL)


class DriverSQL(QSqlTableModel):
    # initialize DB driver table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Driver")
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
    win = DriversWidget()
    win.show()
    sys.exit(app.exec_())
