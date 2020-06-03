from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel


class ClickableQLabel(QLabel):
    clicked = Signal()

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
        QLabel.mousePressEvent(self, QMouseEvent)
