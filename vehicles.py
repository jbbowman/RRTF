# Vehicles Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel


class VehiclesWidget(QWidget):
    # initialize vehicles widget
    def __init__(self):
        super(VehiclesWidget, self).__init__()
        loadUi('UIs/VehiclesWidget.ui', self)  # load VehiclesWidget XML file

        self.initVehiclesTable()

    # attach vehicles table to vehicles widget
    def initVehiclesTable(self):
        self.VehicleSQL = VehicleSQL(self)
        self.vehiclesTable.setModel(self.VehicleSQL)


class VehicleSQL(QSqlTableModel):
    # initialize DB vehicle table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Vehicle")
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
    win = VehiclesWidget()
    win.show()
    sys.exit(app.exec_())