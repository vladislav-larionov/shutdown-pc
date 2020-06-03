
import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QStyle, QMainWindow


class TrayWidget(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon: QStyle, parent: QMainWindow):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(parent.windowTitle())
        self.parent = parent
        menu = QtWidgets.QMenu(parent)
        show_app = menu.addAction("Show")
        show_app.triggered.connect(self.parent.show)
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(self.exit)
        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.parent.show()

    @Slot()
    def exit(self):
        self.hide()
        sys.exit()
