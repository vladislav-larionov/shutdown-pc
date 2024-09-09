# pylint: disable=R0902
"""
Main window of the app
"""
import os
from os.path import expanduser, join, exists

import ifaddr
from PySide2.QtCore import Slot, SIGNAL, Qt
from PySide2.QtNetwork import QTcpServer, QHostAddress, QTcpSocket
from PySide2.QtWidgets import QMainWindow, QTableWidgetItem, QStyle, QApplication

from app.ui.forms.tray_widget import TrayWidget
from app.ui.forms.main_window_form import Ui_MainWindow


class Server(QMainWindow):
    """
    Class that describes main window of the app
    """
    settings_path = join(expanduser("~"), '.shutdown-pc')
    ip_setting_file_path = join(settings_path, 'ip.txt')

    def signals(self):
        """ Connect signals from ui """
        self.connect(self.main_window_ui.start_btn, SIGNAL("clicked()"), self.start_server)
        self.connect(self.main_window_ui.stop_btn, SIGNAL("clicked()"), self.stop)
        self.connect(self.main_window_ui.to_tray_btn, SIGNAL("clicked()"), self.to_tray)
        self.main_window_ui.address_label.clicked.connect(self.copy_address_to_clipboard)
        self.main_window_ui.port_label.clicked.connect(self.copy_port_to_clipboard)
        self.main_window_ui.address.textEdited.connect(self.store_new_ip)

    def __init__(self):
        """ Constructor of widget """
        main_window = QMainWindow()
        self.main_window_ui = Ui_MainWindow()
        self.main_window_ui.setupUi(main_window)
        QMainWindow.__init__(self)
        Ui_MainWindow.setupUi(self.main_window_ui, self)
        self.main_window_ui.clients_table.setColumnCount(2)
        self.main_window_ui.clients_table.setHorizontalHeaderLabels(['ip', 'port'])
        self.load_ip_address()
        self.tray_icon = TrayWidget(self.style().standardIcon(QStyle.SP_ComputerIcon), self)
        self.signals()
        self.server = QTcpServer(self)
        self.server.newConnection.connect(self.new_socket_slot)
        self.start_server()
        self.clients = list()


    def load_ip_address(self):
        if not exists(self.settings_path):
            os.makedirs(self.settings_path, exist_ok=True)
        if exists(self.ip_setting_file_path):
            with open(self.ip_setting_file_path, 'r') as file:
                ip = file.readline().strip()
                print(ip)
                self.main_window_ui.address.setText(ip)


    @Slot()
    def store_new_ip(self):
        print(f"store_new_ip {self.main_window_ui.address.text()}")
        with open(self.ip_setting_file_path, 'w') as file:
            file.write(self.main_window_ui.address.text())


    @Slot()
    def to_tray(self):
        self.hide()
        self.tray_icon.show()

    @Slot()
    def start_server(self):
        if self.server.listen(QHostAddress.AnyIPv4, 9090):
            self.set_start_mode(True)
            self.main_window_ui.log.append("Server is started")
            self.main_window_ui.port.setText(str(self.server.serverPort()))
            self.clients = list()
        else:
            self.main_window_ui.log.append(self.server.errorString())
            self.set_start_mode(False)

    def set_start_mode(self, started):
        self.main_window_ui.start_btn.setEnabled(not started)
        self.main_window_ui.stop_btn.setEnabled(started)

    def new_socket_slot(self):
        socket = self.init_new_client()
        self.clients.append(socket)
        self.log_socket_message(socket, 'Connected')
        self.add_socket_to_clients_table(socket)

    def init_new_client(self):
        socket = self.server.nextPendingConnection()
        socket.readyRead.connect(lambda: self.read_message(socket))
        socket.disconnected.connect(lambda: self.disconnected(socket))
        return socket

    def log_socket_message(self, socket, message):
        peer_address, peer_port = self.socket_address_and_port(socket)
        news = '{}:{} : {}'.format(peer_address, str(peer_port), message)
        self.main_window_ui.log.append(' ' + news + ' ')

    @classmethod
    def socket_address_and_port(cls, socket):
        return socket.peerAddress().toString(), socket.peerPort()

    def add_socket_to_clients_table(self, socket):
        peer_address, peer_port = self.socket_address_and_port(socket)
        row_position = self.main_window_ui.clients_table.rowCount()
        self.main_window_ui.clients_table.insertRow(row_position)
        self.main_window_ui.clients_table.setItem(row_position, 0, QTableWidgetItem(peer_address))
        self.main_window_ui.clients_table.setItem(row_position, 1, QTableWidgetItem(str(peer_port)))

    def read_message(self, socket: QTcpSocket):
        while socket.bytesAvailable():
            datagram = socket.read(socket.bytesAvailable())
            message = datagram.data().decode()
            self.log_socket_message(socket, message)
            self.exec_command(message)
            # Отправляем данные обратно клиенту
            new_datagram = (message + '\0').encode()
            socket.write(new_datagram)

    def exec_command(self, command):
        command = command.split(' ')
        if command[0] == 'cancel':
            command = "shutdown /a"
            os.system(command)
        elif command[0] == 'shutdown':
            command = 'shutdown /s ' + '/t ' + command[1]
            os.system(command)

    def disconnected(self, socket):
        self.log_socket_message(socket, 'Disconnected')
        self.remove_socket_from_clients_table(socket)
        socket.close()

    def remove_socket_from_clients_table(self, socket):
        peer_address, peer_port = self.socket_address_and_port(socket)
        removed = self.main_window_ui.clients_table.findItems(peer_address, Qt.MatchExactly)[0]
        if removed:
            self.main_window_ui.clients_table.removeRow(removed.row())

    @Slot()
    def stop(self):
        self.server.close()
        for client in self.clients:
            client.disconnectFromHost()
        self.set_start_mode(False)
        self.main_window_ui.log.append("Server is stopped")

    @Slot()
    def copy_address_to_clipboard(self):
        self.copy_text_to_clipboard(self.main_window_ui.address.text())

    @Slot()
    def copy_port_to_clipboard(self):
        self.copy_text_to_clipboard(self.main_window_ui.port.text())

    @Slot()
    def copy_text_to_clipboard(self, text):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)
