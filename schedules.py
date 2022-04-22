# Schedules Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel


class SchedulesWidget(QWidget):
    # initialize schedule widget
    def __init__(self):
        super(SchedulesWidget, self).__init__()
        loadUi('UIs/SchedulesWidget.ui', self)  # load SchedulesWidget XML file

        self.initSchedulesTable()

    # attach schedules table to schedules widget
    def initSchedulesTable(self):
        self.ScheduleSQL = ScheduleSQL(self)
        self.schedulesTable.setModel(self.ScheduleSQL)


class ScheduleSQL(QSqlTableModel):
    # initialize DB Schedule table connection
    def __init__(self, parent):
        super(QSqlTableModel, self).__init__(parent)
        self.setTable("Schedule")
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
    win = SchedulesWidget()
    win.show()
    sys.exit(app.exec_())
