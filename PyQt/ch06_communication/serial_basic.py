"""
示例程序：串口通信基础
所属章节：第六章 - 仪器通信基础

功能说明：
    演示串口基础操作：
    - 扫描可用串口
    - 串口参数配置
    - 串口连接测试
    - 基本数据收发

运行方式：
    python serial_basic.py

注意：
    需要安装 pyserial: pip install pyserial
    如果没有真实串口，程序会使用模拟模式运行
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QSpinBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt

# 尝试导入串口库
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("警告: pyserial 未安装，使用模拟模式")


class SerialBasicDemo(QMainWindow):
    """串口基础演示"""
    
    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("串口通信基础")
        self.setMinimumSize(700, 550)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 状态提示
        if not SERIAL_AVAILABLE:
            warning = QLabel("⚠️ pyserial 未安装，运行: pip install pyserial")
            warning.setStyleSheet("""
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
            """)
            main_layout.addWidget(warning)
        
        # 串口配置
        main_layout.addWidget(self.create_config_group())
        
        # 操作按钮
        main_layout.addWidget(self.create_action_group())
        
        # 日志输出
        main_layout.addWidget(self.create_log_group())
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f4f8; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #27ae60;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #27ae60; }
            QPushButton:disabled { background-color: #bdc3c7; }
            QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                min-width: 120px;
            }
        """)
        
        # 初始扫描串口
        self.scan_ports()
    
    def create_config_group(self) -> QGroupBox:
        """创建配置组"""
        group = QGroupBox("串口配置")
        layout = QFormLayout()
        
        # 端口选择
        port_layout = QHBoxLayout()
        self.combo_port = QComboBox()
        self.combo_port.setMinimumWidth(200)
        port_layout.addWidget(self.combo_port)
        
        btn_scan = QPushButton("🔄 扫描")
        btn_scan.setFixedWidth(80)
        btn_scan.clicked.connect(self.scan_ports)
        port_layout.addWidget(btn_scan)
        port_layout.addStretch()
        
        layout.addRow("端口:", port_layout)
        
        # 波特率
        self.combo_baud = QComboBox()
        self.combo_baud.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.combo_baud.setCurrentText('9600')
        layout.addRow("波特率:", self.combo_baud)
        
        # 数据位
        self.combo_databits = QComboBox()
        self.combo_databits.addItems(['5', '6', '7', '8'])
        self.combo_databits.setCurrentText('8')
        layout.addRow("数据位:", self.combo_databits)
        
        # 校验位
        self.combo_parity = QComboBox()
        self.combo_parity.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        layout.addRow("校验位:", self.combo_parity)
        
        # 停止位
        self.combo_stopbits = QComboBox()
        self.combo_stopbits.addItems(['1', '1.5', '2'])
        layout.addRow("停止位:", self.combo_stopbits)
        
        group.setLayout(layout)
        return group
    
    def create_action_group(self) -> QGroupBox:
        """创建操作组"""
        group = QGroupBox("操作")
        layout = QHBoxLayout()
        
        self.btn_connect = QPushButton("🔌 连接")
        self.btn_connect.clicked.connect(self.toggle_connection)
        layout.addWidget(self.btn_connect)
        
        self.btn_test = QPushButton("📡 发送测试命令")
        self.btn_test.setEnabled(False)
        self.btn_test.clicked.connect(self.send_test_command)
        layout.addWidget(self.btn_test)
        
        btn_clear = QPushButton("🗑️ 清空日志")
        btn_clear.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(btn_clear)
        
        layout.addStretch()
        
        # 连接状态
        self.label_status = QLabel("● 未连接")
        self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(self.label_status)
        
        group.setLayout(layout)
        return group
    
    def create_log_group(self) -> QGroupBox:
        """创建日志组"""
        group = QGroupBox("通信日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, 'Courier New', monospace;
                font-size: 12px;
                background-color: #1e272e;
                color: #d2dae2;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def scan_ports(self):
        """扫描可用串口"""
        self.combo_port.clear()
        
        if SERIAL_AVAILABLE:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                self.combo_port.addItem(f"{port.device} - {port.description}", port.device)
            
            if ports:
                self.log(f"找到 {len(ports)} 个串口")
            else:
                self.log("未找到可用串口")
                self.combo_port.addItem("(无可用串口)")
        else:
            # 模拟模式
            self.combo_port.addItem("COM1 - 模拟串口", "COM1")
            self.combo_port.addItem("COM2 - 模拟串口", "COM2")
            self.log("模拟模式: 添加虚拟串口")
    
    def toggle_connection(self):
        """切换连接状态"""
        if self.serial_port and self.serial_port.is_open:
            self.disconnect_serial()
        else:
            self.connect_serial()
    
    def connect_serial(self):
        """连接串口"""
        port = self.combo_port.currentData()
        if not port:
            QMessageBox.warning(self, "警告", "请选择一个串口")
            return
        
        # 获取配置
        baudrate = int(self.combo_baud.currentText())
        databits = int(self.combo_databits.currentText())
        parity_map = {'None': 'N', 'Even': 'E', 'Odd': 'O', 'Mark': 'M', 'Space': 'S'}
        parity = parity_map[self.combo_parity.currentText()]
        stopbits_map = {'1': 1, '1.5': 1.5, '2': 2}
        stopbits = stopbits_map[self.combo_stopbits.currentText()]
        
        if SERIAL_AVAILABLE:
            try:
                self.serial_port = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=databits,
                    parity=parity,
                    stopbits=stopbits,
                    timeout=1
                )
                
                self.log(f"已连接到 {port}")
                self.log(f"  波特率: {baudrate}")
                self.log(f"  数据位: {databits}")
                self.log(f"  校验位: {self.combo_parity.currentText()}")
                self.log(f"  停止位: {stopbits}")
                
                self.update_connection_state(True)
                
            except Exception as e:
                QMessageBox.critical(self, "连接失败", str(e))
                self.log(f"连接失败: {e}")
        else:
            # 模拟模式
            self.log(f"[模拟] 已连接到 {port}")
            self.log(f"  波特率: {baudrate}, 数据位: {databits}")
            
            # 创建模拟对象
            class MockSerial:
                is_open = True
                def close(self): self.is_open = False
                def write(self, data): pass
                def readline(self): return b"*IDN? Response: Simulated Device\r\n"
            
            self.serial_port = MockSerial()
            self.update_connection_state(True)
    
    def disconnect_serial(self):
        """断开串口"""
        if self.serial_port:
            port_name = getattr(self.serial_port, 'port', 'Unknown')
            self.serial_port.close()
            self.serial_port = None
            self.log(f"已断开 {port_name}")
        
        self.update_connection_state(False)
    
    def update_connection_state(self, connected: bool):
        """更新连接状态UI"""
        if connected:
            self.btn_connect.setText("⏏️ 断开")
            self.btn_connect.setStyleSheet("background-color: #e74c3c;")
            self.btn_test.setEnabled(True)
            self.label_status.setText("● 已连接")
            self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.btn_connect.setText("🔌 连接")
            self.btn_connect.setStyleSheet("background-color: #2ecc71;")
            self.btn_test.setEnabled(False)
            self.label_status.setText("● 未连接")
            self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def send_test_command(self):
        """发送测试命令"""
        if not self.serial_port or not self.serial_port.is_open:
            return
        
        # 发送标准SCPI查询命令
        command = b'*IDN?\n'
        self.log(f">>> 发送: {command}")
        
        try:
            if SERIAL_AVAILABLE:
                self.serial_port.write(command)
                response = self.serial_port.readline()
            else:
                response = self.serial_port.readline()
            
            if response:
                self.log(f"<<< 接收: {response.decode('ascii', errors='replace')}")
            else:
                self.log("<<< 接收: (无响应/超时)")
                
        except Exception as e:
            self.log(f"错误: {e}")
    
    def log(self, message: str):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.append(f"[{time_str}] {message}")
    
    def closeEvent(self, event):
        """关闭窗口时断开串口"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = SerialBasicDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

