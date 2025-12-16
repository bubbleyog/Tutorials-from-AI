"""
示例程序：网络通信TCP/UDP
所属章节：第六章 - 仪器通信基础

功能说明：
    演示网络通信功能：
    - TCP客户端连接
    - UDP发送/接收
    - 使用QTcpSocket异步通信
    - 仪器网络控制示例

运行方式：
    python network_comm.py
"""

import sys
import socket
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, QFormLayout,
    QSpinBox, QComboBox, QTabWidget, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtNetwork import QTcpSocket, QUdpSocket, QHostAddress, QAbstractSocket


class TcpClientThread(QThread):
    """TCP客户端线程（阻塞模式）"""
    
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    data_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.send_queue = []
    
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(0.1)
            
            self.connected.emit()
            self.running = True
            
            while self.running:
                # 处理发送队列
                while self.send_queue:
                    data = self.send_queue.pop(0)
                    self.socket.sendall(data)
                
                # 接收数据
                try:
                    data = self.socket.recv(4096)
                    if data:
                        self.data_received.emit(data)
                    elif data == b'':
                        break
                except socket.timeout:
                    pass
                
                self.msleep(10)
                
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if self.socket:
                self.socket.close()
            self.disconnected.emit()
    
    def send(self, data: bytes):
        self.send_queue.append(data)
    
    def stop(self):
        self.running = False
        self.wait(2000)


class NetworkCommDemo(QMainWindow):
    """网络通信演示"""
    
    def __init__(self):
        super().__init__()
        self.tcp_thread = None
        self.tcp_socket = None
        self.udp_socket = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("网络通信 - TCP/UDP")
        self.setMinimumSize(800, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 使用标签页
        tabs = QTabWidget()
        tabs.addTab(self.create_tcp_tab(), "TCP 客户端")
        tabs.addTab(self.create_udp_tab(), "UDP 通信")
        tabs.addTab(self.create_qt_network_tab(), "Qt网络 (异步)")
        
        main_layout.addWidget(tabs)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #8e44ad;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8e44ad; }
            QPushButton:disabled { background-color: #bdc3c7; }
            QLineEdit, QSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 2px solid #9b59b6;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #9b59b6;
                color: white;
            }
        """)
    
    def create_tcp_tab(self) -> QWidget:
        """TCP客户端标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 连接设置
        conn_group = QGroupBox("连接设置")
        conn_layout = QHBoxLayout()
        
        conn_layout.addWidget(QLabel("主机:"))
        self.tcp_host = QLineEdit("127.0.0.1")
        self.tcp_host.setFixedWidth(150)
        conn_layout.addWidget(self.tcp_host)
        
        conn_layout.addWidget(QLabel("端口:"))
        self.tcp_port = QSpinBox()
        self.tcp_port.setRange(1, 65535)
        self.tcp_port.setValue(5000)
        conn_layout.addWidget(self.tcp_port)
        
        conn_layout.addStretch()
        
        self.btn_tcp_connect = QPushButton("连接")
        self.btn_tcp_connect.clicked.connect(self.toggle_tcp_connection)
        conn_layout.addWidget(self.btn_tcp_connect)
        
        self.label_tcp_status = QLabel("● 未连接")
        self.label_tcp_status.setStyleSheet("color: #e74c3c;")
        conn_layout.addWidget(self.label_tcp_status)
        
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        # 接收区
        recv_group = QGroupBox("接收")
        recv_layout = QVBoxLayout()
        self.tcp_receive = QTextEdit()
        self.tcp_receive.setReadOnly(True)
        self.tcp_receive.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        recv_layout.addWidget(self.tcp_receive)
        recv_group.setLayout(recv_layout)
        layout.addWidget(recv_group)
        
        # 发送区
        send_group = QGroupBox("发送")
        send_layout = QHBoxLayout()
        
        self.tcp_send_input = QLineEdit()
        self.tcp_send_input.setPlaceholderText("输入要发送的数据...")
        self.tcp_send_input.returnPressed.connect(self.tcp_send)
        send_layout.addWidget(self.tcp_send_input)
        
        self.check_tcp_newline = QCheckBox("添加换行")
        self.check_tcp_newline.setChecked(True)
        send_layout.addWidget(self.check_tcp_newline)
        
        self.btn_tcp_send = QPushButton("发送")
        self.btn_tcp_send.setEnabled(False)
        self.btn_tcp_send.clicked.connect(self.tcp_send)
        send_layout.addWidget(self.btn_tcp_send)
        
        send_group.setLayout(send_layout)
        layout.addWidget(send_group)
        
        return tab
    
    def create_udp_tab(self) -> QWidget:
        """UDP通信标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 本地设置
        local_group = QGroupBox("本地设置")
        local_layout = QHBoxLayout()
        
        local_layout.addWidget(QLabel("监听端口:"))
        self.udp_local_port = QSpinBox()
        self.udp_local_port.setRange(1, 65535)
        self.udp_local_port.setValue(5001)
        local_layout.addWidget(self.udp_local_port)
        
        local_layout.addStretch()
        
        self.btn_udp_bind = QPushButton("开始监听")
        self.btn_udp_bind.clicked.connect(self.toggle_udp_listen)
        local_layout.addWidget(self.btn_udp_bind)
        
        self.label_udp_status = QLabel("● 未监听")
        self.label_udp_status.setStyleSheet("color: #e74c3c;")
        local_layout.addWidget(self.label_udp_status)
        
        local_group.setLayout(local_layout)
        layout.addWidget(local_group)
        
        # 接收区
        recv_group = QGroupBox("接收")
        recv_layout = QVBoxLayout()
        self.udp_receive = QTextEdit()
        self.udp_receive.setReadOnly(True)
        self.udp_receive.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        recv_layout.addWidget(self.udp_receive)
        recv_group.setLayout(recv_layout)
        layout.addWidget(recv_group)
        
        # 发送区
        send_group = QGroupBox("发送")
        send_layout = QVBoxLayout()
        
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("目标主机:"))
        self.udp_dest_host = QLineEdit("127.0.0.1")
        self.udp_dest_host.setFixedWidth(150)
        dest_layout.addWidget(self.udp_dest_host)
        
        dest_layout.addWidget(QLabel("目标端口:"))
        self.udp_dest_port = QSpinBox()
        self.udp_dest_port.setRange(1, 65535)
        self.udp_dest_port.setValue(5002)
        dest_layout.addWidget(self.udp_dest_port)
        dest_layout.addStretch()
        send_layout.addLayout(dest_layout)
        
        input_layout = QHBoxLayout()
        self.udp_send_input = QLineEdit()
        self.udp_send_input.setPlaceholderText("输入要发送的数据...")
        input_layout.addWidget(self.udp_send_input)
        
        btn_udp_send = QPushButton("发送")
        btn_udp_send.clicked.connect(self.udp_send)
        input_layout.addWidget(btn_udp_send)
        send_layout.addLayout(input_layout)
        
        send_group.setLayout(send_layout)
        layout.addWidget(send_group)
        
        return tab
    
    def create_qt_network_tab(self) -> QWidget:
        """Qt网络标签页（异步）"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel(
            "💡 使用 QTcpSocket 进行异步网络通信，无需单独的线程。\n"
            "   适合简单的仪器控制场景。"
        )
        info.setStyleSheet("""
            background-color: #e8f4f8;
            padding: 10px;
            border-radius: 5px;
            color: #2c3e50;
        """)
        layout.addWidget(info)
        
        # 连接设置
        conn_group = QGroupBox("QTcpSocket 连接")
        conn_layout = QHBoxLayout()
        
        conn_layout.addWidget(QLabel("主机:"))
        self.qt_host = QLineEdit("127.0.0.1")
        self.qt_host.setFixedWidth(150)
        conn_layout.addWidget(self.qt_host)
        
        conn_layout.addWidget(QLabel("端口:"))
        self.qt_port = QSpinBox()
        self.qt_port.setRange(1, 65535)
        self.qt_port.setValue(5000)
        conn_layout.addWidget(self.qt_port)
        
        conn_layout.addStretch()
        
        self.btn_qt_connect = QPushButton("连接")
        self.btn_qt_connect.clicked.connect(self.toggle_qt_connection)
        conn_layout.addWidget(self.btn_qt_connect)
        
        self.label_qt_status = QLabel("● 未连接")
        self.label_qt_status.setStyleSheet("color: #e74c3c;")
        conn_layout.addWidget(self.label_qt_status)
        
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        # 日志
        log_group = QGroupBox("通信日志")
        log_layout = QVBoxLayout()
        self.qt_log = QTextEdit()
        self.qt_log.setReadOnly(True)
        self.qt_log.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        log_layout.addWidget(self.qt_log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # 发送
        send_layout = QHBoxLayout()
        self.qt_send_input = QLineEdit()
        self.qt_send_input.setPlaceholderText("输入命令...")
        send_layout.addWidget(self.qt_send_input)
        
        self.btn_qt_send = QPushButton("发送")
        self.btn_qt_send.setEnabled(False)
        self.btn_qt_send.clicked.connect(self.qt_send)
        send_layout.addWidget(self.btn_qt_send)
        
        layout.addLayout(send_layout)
        
        # 初始化QTcpSocket
        self.tcp_socket = QTcpSocket(self)
        self.tcp_socket.connected.connect(self.on_qt_connected)
        self.tcp_socket.disconnected.connect(self.on_qt_disconnected)
        self.tcp_socket.readyRead.connect(self.on_qt_ready_read)
        self.tcp_socket.errorOccurred.connect(self.on_qt_error)
        
        return tab
    
    # ========== TCP 阻塞模式 ==========
    
    def toggle_tcp_connection(self):
        """切换TCP连接"""
        if self.tcp_thread and self.tcp_thread.isRunning():
            self.tcp_thread.stop()
            self.tcp_thread = None
        else:
            host = self.tcp_host.text()
            port = self.tcp_port.value()
            
            self.tcp_thread = TcpClientThread(host, port)
            self.tcp_thread.connected.connect(self.on_tcp_connected)
            self.tcp_thread.disconnected.connect(self.on_tcp_disconnected)
            self.tcp_thread.data_received.connect(self.on_tcp_data)
            self.tcp_thread.error_occurred.connect(self.on_tcp_error)
            self.tcp_thread.start()
            
            self.log_tcp(f"正在连接 {host}:{port}...")
    
    def on_tcp_connected(self):
        self.btn_tcp_connect.setText("断开")
        self.btn_tcp_send.setEnabled(True)
        self.label_tcp_status.setText("● 已连接")
        self.label_tcp_status.setStyleSheet("color: #27ae60;")
        self.log_tcp("已连接")
    
    def on_tcp_disconnected(self):
        self.btn_tcp_connect.setText("连接")
        self.btn_tcp_send.setEnabled(False)
        self.label_tcp_status.setText("● 未连接")
        self.label_tcp_status.setStyleSheet("color: #e74c3c;")
        self.log_tcp("已断开")
    
    def on_tcp_data(self, data: bytes):
        text = data.decode('ascii', errors='replace')
        self.log_tcp(f"← {text}")
    
    def on_tcp_error(self, error: str):
        self.log_tcp(f"错误: {error}")
    
    def tcp_send(self):
        text = self.tcp_send_input.text()
        if not text or not self.tcp_thread:
            return
        
        data = text.encode('ascii')
        if self.check_tcp_newline.isChecked():
            data += b'\n'
        
        self.tcp_thread.send(data)
        self.log_tcp(f"→ {text}")
        self.tcp_send_input.clear()
    
    def log_tcp(self, msg: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.tcp_receive.append(f"[{time_str}] {msg}")
    
    # ========== UDP ==========
    
    def toggle_udp_listen(self):
        """切换UDP监听"""
        if self.udp_socket:
            self.udp_socket.close()
            self.udp_socket = None
            self.btn_udp_bind.setText("开始监听")
            self.label_udp_status.setText("● 未监听")
            self.label_udp_status.setStyleSheet("color: #e74c3c;")
            self.log_udp("停止监听")
        else:
            self.udp_socket = QUdpSocket(self)
            port = self.udp_local_port.value()
            
            if self.udp_socket.bind(QHostAddress.SpecialAddress.Any, port):
                self.udp_socket.readyRead.connect(self.on_udp_ready_read)
                self.btn_udp_bind.setText("停止监听")
                self.label_udp_status.setText(f"● 监听端口 {port}")
                self.label_udp_status.setStyleSheet("color: #27ae60;")
                self.log_udp(f"开始监听端口 {port}")
            else:
                self.log_udp(f"绑定端口 {port} 失败")
                self.udp_socket = None
    
    def on_udp_ready_read(self):
        while self.udp_socket.hasPendingDatagrams():
            data, host, port = self.udp_socket.readDatagram(
                self.udp_socket.pendingDatagramSize()
            )
            text = bytes(data).decode('ascii', errors='replace')
            self.log_udp(f"← [{host.toString()}:{port}] {text}")
    
    def udp_send(self):
        text = self.udp_send_input.text()
        if not text:
            return
        
        host = self.udp_dest_host.text()
        port = self.udp_dest_port.value()
        
        sock = QUdpSocket()
        data = text.encode('ascii') + b'\n'
        sock.writeDatagram(data, QHostAddress(host), port)
        sock.close()
        
        self.log_udp(f"→ [{host}:{port}] {text}")
        self.udp_send_input.clear()
    
    def log_udp(self, msg: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.udp_receive.append(f"[{time_str}] {msg}")
    
    # ========== Qt网络（异步） ==========
    
    def toggle_qt_connection(self):
        """切换Qt网络连接"""
        if self.tcp_socket.state() == QAbstractSocket.SocketState.ConnectedState:
            self.tcp_socket.disconnectFromHost()
        else:
            host = self.qt_host.text()
            port = self.qt_port.value()
            self.log_qt(f"正在连接 {host}:{port}...")
            self.tcp_socket.connectToHost(host, port)
    
    def on_qt_connected(self):
        self.btn_qt_connect.setText("断开")
        self.btn_qt_send.setEnabled(True)
        self.label_qt_status.setText("● 已连接")
        self.label_qt_status.setStyleSheet("color: #27ae60;")
        self.log_qt("已连接")
    
    def on_qt_disconnected(self):
        self.btn_qt_connect.setText("连接")
        self.btn_qt_send.setEnabled(False)
        self.label_qt_status.setText("● 未连接")
        self.label_qt_status.setStyleSheet("color: #e74c3c;")
        self.log_qt("已断开")
    
    def on_qt_ready_read(self):
        data = self.tcp_socket.readAll().data()
        text = data.decode('ascii', errors='replace')
        self.log_qt(f"← {text}")
    
    def on_qt_error(self, error):
        self.log_qt(f"错误: {self.tcp_socket.errorString()}")
    
    def qt_send(self):
        text = self.qt_send_input.text()
        if not text:
            return
        
        data = text.encode('ascii') + b'\n'
        self.tcp_socket.write(data)
        self.log_qt(f"→ {text}")
        self.qt_send_input.clear()
    
    def log_qt(self, msg: str):
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.qt_log.append(f"[{time_str}] {msg}")
    
    def closeEvent(self, event):
        """关闭窗口"""
        if self.tcp_thread:
            self.tcp_thread.stop()
        if self.tcp_socket:
            self.tcp_socket.close()
        if self.udp_socket:
            self.udp_socket.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = NetworkCommDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

