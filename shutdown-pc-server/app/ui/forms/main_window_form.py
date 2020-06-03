# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_form.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from ui.forms.clickable_qlabel import ClickableQLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(437, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 20, 281, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.start_btn = QPushButton(self.horizontalLayoutWidget)
        self.start_btn.setObjectName(u"start_btn")

        self.horizontalLayout.addWidget(self.start_btn)

        self.stop_btn = QPushButton(self.horizontalLayoutWidget)
        self.stop_btn.setObjectName(u"stop_btn")

        self.horizontalLayout.addWidget(self.stop_btn)

        self.to_tray_btn = QPushButton(self.horizontalLayoutWidget)
        self.to_tray_btn.setObjectName(u"to_tray_btn")

        self.horizontalLayout.addWidget(self.to_tray_btn)

        self.log = QTextBrowser(self.centralwidget)
        self.log.setObjectName(u"log")
        self.log.setGeometry(QRect(10, 270, 411, 201))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 110, 47, 13))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 250, 47, 13))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 70, 184, 22))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.address_label = ClickableQLabel(self.layoutWidget)
        self.address_label.setObjectName(u"address_label")
        self.address_label.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.address_label)

        self.address = QLineEdit(self.layoutWidget)
        self.address.setObjectName(u"address")
        self.address.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.address)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(210, 70, 165, 22))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.port_label = ClickableQLabel(self.layoutWidget1)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.port_label)

        self.port = QLineEdit(self.layoutWidget1)
        self.port.setObjectName(u"port")
        self.port.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.port)

        self.clients_table = QTableWidget(self.centralwidget)
        self.clients_table.setObjectName(u"clients_table")
        self.clients_table.setGeometry(QRect(15, 140, 401, 101))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 437, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ShutdownPC Server", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.to_tray_btn.setText(QCoreApplication.translate("MainWindow", u"to tray", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Clients:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Log:", None))
#if QT_CONFIG(tooltip)
        self.address_label.setToolTip(QCoreApplication.translate("MainWindow", u"Click to copy", None))
#endif // QT_CONFIG(tooltip)
        self.address_label.setText(QCoreApplication.translate("MainWindow", u"Address:", None))
#if QT_CONFIG(tooltip)
        self.port_label.setToolTip(QCoreApplication.translate("MainWindow", u"Click to copy", None))
#endif // QT_CONFIG(tooltip)
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
    # retranslateUi

