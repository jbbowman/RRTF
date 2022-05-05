# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SchedulesWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SchedulesWidget(object):
    def setupUi(self, SchedulesWidget):
        SchedulesWidget.setObjectName("SchedulesWidget")
        SchedulesWidget.resize(827, 654)
        self.schedulesWidgetLayout = QtWidgets.QVBoxLayout(SchedulesWidget)
        self.schedulesWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.schedulesWidgetLayout.setSpacing(0)
#        self.SchedulesLayout.setObjectName("SchedulesLayout")
        self.schedulesTable = QtWidgets.QTableView(SchedulesWidget)
        self.schedulesTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.schedulesTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.schedulesTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.schedulesTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.schedulesTable.setSortingEnabled(True)
        self.schedulesTable.setCornerButtonEnabled(False)
        self.schedulesTable.setObjectName("schedulesTable")
        self.schedulesTable.horizontalHeader().setDefaultSectionSize(140)
        self.schedulesTable.horizontalHeader().setStretchLastSection(True)
        self.schedulesTable.verticalHeader().setVisible(False)
        self.schedulesTable.verticalHeader().setDefaultSectionSize(32)
        self.schedulesTable.verticalHeader().setMinimumSectionSize(32)
        self.schedulesWidgetLayout.addWidget(self.schedulesTable)
        self.bottomPanel = QtWidgets.QWidget(SchedulesWidget)
        self.bottomPanel.setStyleSheet("QWidget#bottomPanel {background-color: rgb(225, 225, 225);}\n"
"QWidget#dateLabel {background-color: rgb(225, 225, 225);}\n"
"QWidget#driverLabel {background-color: rgb(225, 225, 225);}\n"
"QWidget#vehicleLabel {background-color: rgb(225, 225, 225);}\n"
"QWidget#searchLabel {background-color: rgb(225, 225, 225);}")
        self.bottomPanel.setObjectName("bottomPanel")
        self.bottomPanelLayout = QtWidgets.QHBoxLayout(self.bottomPanel)
        self.bottomPanelLayout.setObjectName("bottomPanelLayout")
        self.dateLabel = QtWidgets.QLabel(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.bottomPanelLayout.addWidget(self.dateLabel, 0, QtCore.Qt.AlignVCenter)
        self.dateEdit1 = QtWidgets.QDateEdit(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.dateEdit1.setFont(font)
        self.dateEdit1.setStyleSheet("")
        self.dateEdit1.setMinimumDate(QtCore.QDate(2022, 1, 1))
        self.dateEdit1.setObjectName("dateEdit1")
        self.bottomPanelLayout.addWidget(self.dateEdit1)
        self.dash = QtWidgets.QFrame(self.bottomPanel)
        self.dash.setMinimumSize(QtCore.QSize(10, 0))
        self.dash.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.dash.setFrameShape(QtWidgets.QFrame.HLine)
        self.dash.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.dash.setObjectName("dash")
        self.bottomPanelLayout.addWidget(self.dash)
        self.dateEdit2 = QtWidgets.QDateEdit(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.dateEdit2.setFont(font)
        self.dateEdit2.setStyleSheet("")
        self.dateEdit2.setMinimumDate(QtCore.QDate(2022, 1, 1))
        self.dateEdit2.setObjectName("dateEdit2")
        self.bottomPanelLayout.addWidget(self.dateEdit2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.bottomPanelLayout.addItem(spacerItem)
        self.driverLabel = QtWidgets.QLabel(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.driverLabel.setFont(font)
        self.driverLabel.setObjectName("driverLabel")
        self.bottomPanelLayout.addWidget(self.driverLabel, 0, QtCore.Qt.AlignVCenter)
        self.driverSearch = QtWidgets.QComboBox(self.bottomPanel)
        self.driverSearch.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.driverSearch.setFont(font)
        self.driverSearch.setStyleSheet("")
        self.driverSearch.setObjectName("driverSearch")
        self.driverSearch.addItem("")
        self.driverSearch.addItem("")
        self.driverSearch.addItem("")
        self.driverSearch.addItem("")
        self.bottomPanelLayout.addWidget(self.driverSearch)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.bottomPanelLayout.addItem(spacerItem1)
        self.vehicleLabel = QtWidgets.QLabel(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.vehicleLabel.setFont(font)
        self.vehicleLabel.setObjectName("vehicleLabel")
        self.bottomPanelLayout.addWidget(self.vehicleLabel, 0, QtCore.Qt.AlignVCenter)
        self.vehicleSearch = QtWidgets.QComboBox(self.bottomPanel)
        self.vehicleSearch.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.vehicleSearch.setFont(font)
        self.vehicleSearch.setStyleSheet("")
        self.vehicleSearch.setObjectName("vehicleSearch")
        self.vehicleSearch.addItem("")
        self.vehicleSearch.addItem("")
        self.vehicleSearch.addItem("")
        self.vehicleSearch.addItem("")
        self.bottomPanelLayout.addWidget(self.vehicleSearch)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottomPanelLayout.addItem(spacerItem2)
        self.searchLabel = QtWidgets.QLabel(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName("searchLabel")
        self.bottomPanelLayout.addWidget(self.searchLabel, 0, QtCore.Qt.AlignVCenter)
        self.searchBox = QtWidgets.QLineEdit(self.bottomPanel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setItalic(True)
        self.searchBox.setFont(font)
        self.searchBox.setStyleSheet("")
        self.searchBox.setObjectName("searchBox")
        self.bottomPanelLayout.addWidget(self.searchBox)
        self.searchButton = QtWidgets.QCommandLinkButton(self.bottomPanel)
        self.searchButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.searchButton.setStyleSheet("")
        self.searchButton.setObjectName("searchButton")
        self.bottomPanelLayout.addWidget(self.searchButton, 0, QtCore.Qt.AlignVCenter)
        self.schedulesWidgetLayout.addWidget(self.bottomPanel)

        self.retranslateUi(SchedulesWidget)
        QtCore.QMetaObject.connectSlotsByName(SchedulesWidget)

    def retranslateUi(self, SchedulesWidget):
        _translate = QtCore.QCoreApplication.translate
        SchedulesWidget.setWindowTitle(_translate("SchedulesWidget", "SchedulesWidget"))
        self.dateLabel.setText(_translate("SchedulesWidget", "Date:"))
        self.dateEdit1.setToolTip(_translate("SchedulesWidget", "Search from"))
        self.dateEdit2.setToolTip(_translate("SchedulesWidget", "Search to"))
        self.driverLabel.setText(_translate("SchedulesWidget", "Driver:"))
        self.driverSearch.setToolTip(_translate("SchedulesWidget", "Search by driver"))
        self.driverSearch.setItemText(0, _translate("SchedulesWidget", "All Drivers"))
        self.driverSearch.setItemText(1, _translate("SchedulesWidget", "Driver1"))
        self.driverSearch.setItemText(2, _translate("SchedulesWidget", "Driver2"))
        self.driverSearch.setItemText(3, _translate("SchedulesWidget", "Driver3"))
        self.vehicleLabel.setText(_translate("SchedulesWidget", "Vehicle:"))
        self.vehicleSearch.setToolTip(_translate("SchedulesWidget", "Search by vehicle"))
        self.vehicleSearch.setItemText(0, _translate("SchedulesWidget", "All Vehicles"))
        self.vehicleSearch.setItemText(1, _translate("SchedulesWidget", "Vehicle1"))
        self.vehicleSearch.setItemText(2, _translate("SchedulesWidget", "Vehicle2"))
        self.vehicleSearch.setItemText(3, _translate("SchedulesWidget", "Vehicle3"))
        self.searchLabel.setText(_translate("SchedulesWidget", "Search:"))
        self.searchBox.setToolTip(_translate("SchedulesWidget", "Search invoice IDs"))
        self.searchButton.setToolTip(_translate("SchedulesWidget", "Go"))
