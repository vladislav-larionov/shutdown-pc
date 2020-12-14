
"""
Starting point of the app where window displays
"""
import sys

from PySide2.QtWidgets import QApplication

from ui.app import Server

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Server()
    widget.show()
    widget.to_tray()
    sys.exit(app.exec_())
