# Settings Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class SettingsWidget(QWidget):
    # initialize settings widget
    def __init__(self):
        super(SettingsWidget, self).__init__()
        loadUi('UIs/SettingsWidget.ui', self)  # load SettingsWidget XML file

        # TODO add customization features

        # TODO add adjustable work hours per item


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = SettingsWidget()
    win.show()
    sys.exit(app.exec_())