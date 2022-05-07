# About Widget

# import PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class AboutWidget(QWidget):
    # initialize about widget
    def __init__(self):
        super(AboutWidget, self).__init__()
        # TODO loadUi('UIs/AboutWidget.ui', self)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = AboutWidget()
    win.show()
    sys.exit(app.exec_())