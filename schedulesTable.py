# import PyQt5
from PyQt5.QtWidgets import QTableView
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import Qt


class Table(QTableView):
    def __init__(self):
        super(Table, self).__init__()
        self.SQL = SQL(self)

        self.initUI()

    def initUI(self):
        self.setEditTriggers(self.DoubleClicked)
        self.setSelectionBehavior(self.SelectRows)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setSortingEnabled(True)
        self.setCornerButtonEnabled(False)
        self.horizontalHeader().setDefaultSectionSize(140)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(32)
        self.verticalHeader().setMinimumSectionSize(32)
        self.setModel(self.SQL)


class SQL(QSqlTableModel):
    def __init__(self, parent):
        super(SQL, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTable("Schedule")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.setColumns()
        self.select()

    def setColumns(self):
        columns = ['Schedule ID', 'Driver ID', 'Vehicle ID', 'Execution Date', 'Stops', 'Nursery Items', 'Loading Hours',
                   'Work Hours', 'Drive Hours', 'Total Hours', 'Notes']

        for i in range(len(columns)):
            self.setHeaderData(i, Qt.Horizontal, columns[i])


if __name__ == "__main__":
    import sys, database
    from PyQt5.QtWidgets import QApplication, QMessageBox

    try:
        app = QApplication(sys.argv)
        database.DBConnection()
        win = Table()
        win.show()
        sys.exit(app.exec_())

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred:\n {exception}')
        sys.exit(1)
