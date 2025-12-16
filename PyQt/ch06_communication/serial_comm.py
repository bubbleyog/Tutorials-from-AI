"""
示例程序：串口数据收发
所属章节：第六章 - 仪器通信基础

功能说明：
    演示完整的串口通信功能：
    - 使用QThread进行后台串口读取
    - 发送ASCII和HEX数据
    - 数据显示（ASCII/HEX模式）
    - 定时发送功能
    - 实时数据统计

运行方式：
    python serial_comm.py

注意：
    需要安装 pyserial: pip install pyserial
"""

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QLineEdit, QTextEdit, QCheckBox, QSpinBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer

# 尝试导入串口库
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False


class SerialReaderThread(QThread):
    """串口读取线程"""
    
    data_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = False
    
    def run(self):
        self.running = True
        
        while self.running:
            try:
                if self.serial_port and self.serial_port.is_open:
                    if self.serial_port.in_waiting > 0:
                        data = self.serial_port.read(self.serial_port.in_waiting)
                        if data:
                            self.data_received.emit(data)
                self.msleep(10)  # 10ms轮询间隔
                
            except Exception as e:
                self.error_occurred.emit(str(e))
                break
    
    def stop(self):
        self.running = False
        self.wait(1000)


class SerialCommDemo(QMainWindow):
    """串口通信演示 - 完整功能"""
    
    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.reader_thread = None
        self.tx_count = 0
        self.rx_count = 0
        self.auto_send_timer = QTimer()
        self.auto_send_timer.timeout.connect(self.auto_send)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("串口通信助手")
        self.setMinimumSize(900, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 顶部工具栏
        main_layout.addWidget(self.create_toolbar())
        
        # 主内容区域（使用分割器）
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 接收区
        splitter.addWidget(self.create_receive_group())
        
        # 发送区
        splitter.addWidget(self.create_send_group())
        
        splitter.setSizes([400, 200])
        main_layout.addWidget(splitter)
        
        # 状态栏
        main_layout.addWidget(self.create_status_bar())
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2980b9;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:disabled { background-color: #bdc3c7; }
            QPushButton:checked { background-color: #27ae60; }
            QComboBox, QSpinBox, QLineEdit {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
        
        self.scan_ports()
    
    def create_toolbar(self) -> QWidget:
        """创建工具栏"""
        toolbar = QWidget()
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 端口选择
        layout.addWidget(QLabel("端口:"))
        self.combo_port = QComboBox()
        self.combo_port.setMinimumWidth(180)
        layout.addWidget(self.combo_port)
        
        btn_scan = QPushButton("🔄")
        btn_scan.setFixedWidth(40)
        btn_scan.setToolTip("扫描串口")
        btn_scan.clicked.connect(self.scan_ports)
        layout.addWidget(btn_scan)
        
        # 波特率
        layout.addWidget(QLabel("波特率:"))
        self.combo_baud = QComboBox()
        self.combo_baud.addItems(['9600', '19200', '38400', '57600', '115200', '230400'])
        self.combo_baud.setCurrentText('115200')
        layout.addWidget(self.combo_baud)
        
        # 数据格式
        layout.addWidget(QLabel("格式:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(['8N1', '8E1', '8O1', '7E1', '7O1'])
        layout.addWidget(self.combo_format)
        
        layout.addStretch()
        
        # 连接按钮
        self.btn_connect = QPushButton("🔌 打开串口")
        self.btn_connect.setCheckable(True)
        self.btn_connect.clicked.connect(self.toggle_connection)
        layout.addWidget(self.btn_connect)
        
        return toolbar
    
    def create_receive_group(self) -> QGroupBox:
        """创建接收区"""
        group = QGroupBox("接收区")
        layout = QVBoxLayout()
        
        # 选项栏
        options = QHBoxLayout()
        
        self.check_hex_display = QCheckBox("HEX显示")
        self.check_hex_display.stateChanged.connect(self.update_display)
        options.addWidget(self.check_hex_display)
        
        self.check_timestamp = QCheckBox("显示时间戳")
        self.check_timestamp.setChecked(True)
        options.addWidget(self.check_timestamp)
        
        self.check_autoscroll = QCheckBox("自动滚动")
        self.check_autoscroll.setChecked(True)
        options.addWidget(self.check_autoscroll)
        
        options.addStretch()
        
        btn_clear = QPushButton("清空")
        btn_clear.clicked.connect(self.clear_receive)
        options.addWidget(btn_clear)
        
        layout.addLayout(options)
        
        # 接收文本框
        self.text_receive = QTextEdit()
        self.text_receive.setReadOnly(True)
        self.text_receive.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.text_receive)
        
        group.setLayout(layout)
        return group
    
    def create_send_group(self) -> QGroupBox:
        """创建发送区"""
        group = QGroupBox("发送区")
        layout = QVBoxLayout()
        
        # 发送选项
        options = QHBoxLayout()
        
        self.check_hex_send = QCheckBox("HEX发送")
        options.addWidget(self.check_hex_send)
        
        self.check_newline = QCheckBox("发送新行")
        self.check_newline.setChecked(True)
        options.addWidget(self.check_newline)
        
        self.combo_newline = QComboBox()
        self.combo_newline.addItems(['\\r\\n', '\\n', '\\r'])
        options.addWidget(self.combo_newline)
        
        options.addStretch()
        
        # 定时发送
        self.check_auto_send = QCheckBox("定时发送")
        self.check_auto_send.stateChanged.connect(self.toggle_auto_send)
        options.addWidget(self.check_auto_send)
        
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(100, 10000)
        self.spin_interval.setValue(1000)
        self.spin_interval.setSuffix(" ms")
        options.addWidget(self.spin_interval)
        
        layout.addLayout(options)
        
        # 发送输入框
        send_layout = QHBoxLayout()
        
        self.line_send = QLineEdit()
        self.line_send.setPlaceholderText("输入要发送的数据...")
        self.line_send.returnPressed.connect(self.send_data)
        send_layout.addWidget(self.line_send)
        
        self.btn_send = QPushButton("发送")
        self.btn_send.setEnabled(False)
        self.btn_send.clicked.connect(self.send_data)
        send_layout.addWidget(self.btn_send)
        
        layout.addLayout(send_layout)
        
        # 快捷命令
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("快捷命令:"))
        
        quick_commands = ['*IDN?', '*RST', '*OPC?', ':SYST:ERR?']
        for cmd in quick_commands:
            btn = QPushButton(cmd)
            btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
            btn.clicked.connect(lambda checked, c=cmd: self.send_quick_command(c))
            quick_layout.addWidget(btn)
        
        quick_layout.addStretch()
        layout.addLayout(quick_layout)
        
        group.setLayout(layout)
        return group
    
    def create_status_bar(self) -> QWidget:
        """创建状态栏"""
        status = QWidget()
        layout = QHBoxLayout(status)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.label_status = QLabel("● 未连接")
        self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(self.label_status)
        
        layout.addStretch()
        
        self.label_tx = QLabel("TX: 0")
        layout.addWidget(self.label_tx)
        
        self.label_rx = QLabel("RX: 0")
        layout.addWidget(self.label_rx)
        
        btn_reset_count = QPushButton("重置计数")
        btn_reset_count.setStyleSheet("padding: 3px 8px; font-size: 11px;")
        btn_reset_count.clicked.connect(self.reset_counts)
        layout.addWidget(btn_reset_count)
        
        return status
    
    def scan_ports(self):
        """扫描串口"""
        self.combo_port.clear()
        
        if SERIAL_AVAILABLE:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                self.combo_port.addItem(f"{port.device}", port.device)
        else:
            self.combo_port.addItem("COM1 (模拟)", "COM1")
    
    def toggle_connection(self, checked: bool):
        """切换连接状态"""
        if checked:
            self.connect_serial()
        else:
            self.disconnect_serial()
    
    def connect_serial(self):
        """连接串口"""
        port = self.combo_port.currentData()
        if not port:
            self.btn_connect.setChecked(False)
            return
        
        baudrate = int(self.combo_baud.currentText())
        format_str = self.combo_format.currentText()
        
        # 解析格式
        databits = int(format_str[0])
        parity = {'N': 'N', 'E': 'E', 'O': 'O'}[format_str[1]]
        stopbits = int(format_str[2])
        
        if SERIAL_AVAILABLE:
            try:
                self.serial_port = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=databits,
                    parity=parity,
                    stopbits=stopbits,
                    timeout=0.1
                )
                
                # 启动读取线程
                self.reader_thread = SerialReaderThread(self.serial_port)
                self.reader_thread.data_received.connect(self.on_data_received)
                self.reader_thread.error_occurred.connect(self.on_error)
                self.reader_thread.start()
                
                self.update_connection_state(True, port)
                
            except Exception as e:
                self.append_receive(f"连接失败: {e}")
                self.btn_connect.setChecked(False)
        else:
            # 模拟模式
            self.update_connection_state(True, port + " (模拟)")
    
    def disconnect_serial(self):
        """断开串口"""
        # 停止定时发送
        self.auto_send_timer.stop()
        self.check_auto_send.setChecked(False)
        
        # 停止读取线程
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        
        # 关闭串口
        if self.serial_port and SERIAL_AVAILABLE:
            self.serial_port.close()
            self.serial_port = None
        
        self.update_connection_state(False)
    
    def update_connection_state(self, connected: bool, port_name: str = ""):
        """更新连接状态"""
        if connected:
            self.btn_connect.setText("🔌 关闭串口")
            self.btn_send.setEnabled(True)
            self.label_status.setText(f"● 已连接 {port_name}")
            self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.btn_connect.setText("🔌 打开串口")
            self.btn_send.setEnabled(False)
            self.label_status.setText("● 未连接")
            self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def on_data_received(self, data: bytes):
        """接收到数据"""
        self.rx_count += len(data)
        self.label_rx.setText(f"RX: {self.rx_count}")
        
        if self.check_hex_display.isChecked():
            text = ' '.join(f'{b:02X}' for b in data)
        else:
            text = data.decode('ascii', errors='replace')
        
        self.append_receive(text, is_rx=True)
    
    def on_error(self, error: str):
        """发生错误"""
        self.append_receive(f"错误: {error}")
        self.btn_connect.setChecked(False)
        self.disconnect_serial()
    
    def send_data(self):
        """发送数据"""
        text = self.line_send.text()
        if not text:
            return
        
        # 构建数据
        if self.check_hex_send.isChecked():
            try:
                data = bytes.fromhex(text.replace(' ', ''))
            except ValueError:
                self.append_receive("HEX格式错误")
                return
        else:
            data = text.encode('ascii')
        
        # 添加换行符
        if self.check_newline.isChecked():
            newline_map = {'\\r\\n': b'\r\n', '\\n': b'\n', '\\r': b'\r'}
            data += newline_map[self.combo_newline.currentText()]
        
        self.send_bytes(data)
        
        # 显示发送内容
        if self.check_hex_send.isChecked():
            display = ' '.join(f'{b:02X}' for b in data)
        else:
            display = text
        self.append_receive(display, is_rx=False)
    
    def send_bytes(self, data: bytes):
        """发送字节"""
        if SERIAL_AVAILABLE and self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data)
        
        self.tx_count += len(data)
        self.label_tx.setText(f"TX: {self.tx_count}")
    
    def send_quick_command(self, cmd: str):
        """发送快捷命令"""
        self.line_send.setText(cmd)
        self.send_data()
    
    def append_receive(self, text: str, is_rx: bool = None):
        """添加到接收区"""
        if self.check_timestamp.isChecked():
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            if is_rx is True:
                prefix = f"[{timestamp}] ← "
            elif is_rx is False:
                prefix = f"[{timestamp}] → "
            else:
                prefix = f"[{timestamp}] "
            text = prefix + text
        
        self.text_receive.append(text.rstrip())
        
        if self.check_autoscroll.isChecked():
            self.text_receive.verticalScrollBar().setValue(
                self.text_receive.verticalScrollBar().maximum()
            )
    
    def clear_receive(self):
        """清空接收区"""
        self.text_receive.clear()
    
    def update_display(self):
        """更新显示模式"""
        # 切换HEX/ASCII显示时可以重新解析缓冲区
        pass
    
    def toggle_auto_send(self, state: int):
        """切换定时发送"""
        if state == Qt.CheckState.Checked.value:
            interval = self.spin_interval.value()
            self.auto_send_timer.start(interval)
        else:
            self.auto_send_timer.stop()
    
    def auto_send(self):
        """自动发送"""
        if self.btn_send.isEnabled():
            self.send_data()
    
    def reset_counts(self):
        """重置计数"""
        self.tx_count = 0
        self.rx_count = 0
        self.label_tx.setText("TX: 0")
        self.label_rx.setText("RX: 0")
    
    def closeEvent(self, event):
        """关闭窗口"""
        self.disconnect_serial()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = SerialCommDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

