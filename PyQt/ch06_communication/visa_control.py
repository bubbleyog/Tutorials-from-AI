"""
示例程序：VISA仪器控制
所属章节：第六章 - 仪器通信基础

功能说明：
    演示PyVISA仪器控制：
    - 扫描VISA资源
    - 连接仪器
    - 发送SCPI命令
    - 查询仪器信息

运行方式：
    python visa_control.py

注意：
    需要安装 pyvisa 和 pyvisa-py:
    pip install pyvisa pyvisa-py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QLineEdit, QTextEdit, QListWidget, QSpinBox, QMessageBox,
    QSplitter
)
from PyQt6.QtCore import Qt

# 尝试导入VISA库
try:
    import pyvisa
    VISA_AVAILABLE = True
except ImportError:
    VISA_AVAILABLE = False
    print("警告: pyvisa 未安装，使用模拟模式")
    print("安装: pip install pyvisa pyvisa-py")


class VisaControlDemo(QMainWindow):
    """VISA仪器控制演示"""
    
    def __init__(self):
        super().__init__()
        self.rm = None
        self.instrument = None
        self.init_ui()
        
        if VISA_AVAILABLE:
            try:
                self.rm = pyvisa.ResourceManager('@py')
            except Exception:
                try:
                    self.rm = pyvisa.ResourceManager()
                except Exception as e:
                    self.log(f"无法创建ResourceManager: {e}")
    
    def init_ui(self):
        self.setWindowTitle("VISA仪器控制")
        self.setMinimumSize(900, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 警告提示
        if not VISA_AVAILABLE:
            warning = QLabel("⚠️ pyvisa 未安装，运行: pip install pyvisa pyvisa-py")
            warning.setStyleSheet("""
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
            """)
            main_layout.addWidget(warning)
        
        # 使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：仪器列表
        splitter.addWidget(self.create_resource_panel())
        
        # 右侧：控制和日志
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self.create_command_panel())
        right_layout.addWidget(self.create_log_panel())
        splitter.addWidget(right_panel)
        
        splitter.setSizes([300, 600])
        main_layout.addWidget(splitter)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f4f8; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #d35400;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d35400; }
            QPushButton:disabled { background-color: #bdc3c7; }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #e67e22;
                color: white;
            }
        """)
    
    def create_resource_panel(self) -> QGroupBox:
        """创建资源面板"""
        group = QGroupBox("VISA资源")
        layout = QVBoxLayout()
        
        # 扫描按钮
        btn_scan = QPushButton("🔍 扫描仪器")
        btn_scan.clicked.connect(self.scan_resources)
        layout.addWidget(btn_scan)
        
        # 资源列表
        self.list_resources = QListWidget()
        self.list_resources.itemDoubleClicked.connect(self.connect_instrument)
        layout.addWidget(self.list_resources)
        
        # 连接按钮
        btn_layout = QHBoxLayout()
        
        self.btn_connect = QPushButton("连接")
        self.btn_connect.clicked.connect(self.connect_instrument)
        btn_layout.addWidget(self.btn_connect)
        
        self.btn_disconnect = QPushButton("断开")
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.clicked.connect(self.disconnect_instrument)
        btn_layout.addWidget(self.btn_disconnect)
        
        layout.addLayout(btn_layout)
        
        # 连接状态
        self.label_status = QLabel("● 未连接")
        self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(self.label_status)
        
        # 仪器信息
        info_layout = QFormLayout()
        self.label_idn = QLabel("-")
        self.label_idn.setWordWrap(True)
        info_layout.addRow("IDN:", self.label_idn)
        layout.addLayout(info_layout)
        
        group.setLayout(layout)
        return group
    
    def create_command_panel(self) -> QGroupBox:
        """创建命令面板"""
        group = QGroupBox("SCPI命令")
        layout = QVBoxLayout()
        
        # 命令输入
        input_layout = QHBoxLayout()
        
        self.line_command = QLineEdit()
        self.line_command.setPlaceholderText("输入SCPI命令，如 *IDN?")
        self.line_command.returnPressed.connect(self.send_command)
        input_layout.addWidget(self.line_command)
        
        self.btn_send = QPushButton("发送")
        self.btn_send.setEnabled(False)
        self.btn_send.clicked.connect(self.send_command)
        input_layout.addWidget(self.btn_send)
        
        self.btn_query = QPushButton("查询")
        self.btn_query.setEnabled(False)
        self.btn_query.clicked.connect(self.query_command)
        input_layout.addWidget(self.btn_query)
        
        layout.addLayout(input_layout)
        
        # 快捷命令
        quick_group = QGroupBox("常用命令")
        quick_layout = QVBoxLayout()
        
        # 通用命令
        row1 = QHBoxLayout()
        for cmd in ['*IDN?', '*RST', '*CLS', '*OPC?', ':SYST:ERR?']:
            btn = QPushButton(cmd)
            btn.setStyleSheet("padding: 5px 10px; font-size: 11px;")
            btn.clicked.connect(lambda c, cmd=cmd: self.quick_query(cmd))
            row1.addWidget(btn)
        quick_layout.addLayout(row1)
        
        # 示波器命令
        quick_layout.addWidget(QLabel("示波器:"))
        row2 = QHBoxLayout()
        scope_cmds = [':RUN', ':STOP', ':SING', ':MEAS:FREQ?', ':MEAS:VPP?']
        for cmd in scope_cmds:
            btn = QPushButton(cmd)
            btn.setStyleSheet("padding: 5px 8px; font-size: 10px;")
            btn.clicked.connect(lambda c, cmd=cmd: self.quick_query(cmd))
            row2.addWidget(btn)
        quick_layout.addLayout(row2)
        
        # 电源命令
        quick_layout.addWidget(QLabel("电源:"))
        row3 = QHBoxLayout()
        psu_cmds = [':OUTP ON', ':OUTP OFF', ':VOLT?', ':CURR?', ':MEAS:ALL?']
        for cmd in psu_cmds:
            btn = QPushButton(cmd)
            btn.setStyleSheet("padding: 5px 8px; font-size: 10px;")
            btn.clicked.connect(lambda c, cmd=cmd: self.quick_query(cmd))
            row3.addWidget(btn)
        quick_layout.addLayout(row3)
        
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
        # 超时设置
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("超时:"))
        self.spin_timeout = QSpinBox()
        self.spin_timeout.setRange(100, 30000)
        self.spin_timeout.setValue(5000)
        self.spin_timeout.setSuffix(" ms")
        timeout_layout.addWidget(self.spin_timeout)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)
        
        group.setLayout(layout)
        return group
    
    def create_log_panel(self) -> QGroupBox:
        """创建日志面板"""
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
            }
        """)
        layout.addWidget(self.log_text)
        
        btn_clear = QPushButton("清空日志")
        btn_clear.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(btn_clear)
        
        group.setLayout(layout)
        return group
    
    def scan_resources(self):
        """扫描VISA资源"""
        self.list_resources.clear()
        
        if VISA_AVAILABLE and self.rm:
            try:
                resources = self.rm.list_resources()
                for res in resources:
                    self.list_resources.addItem(res)
                
                self.log(f"找到 {len(resources)} 个VISA资源")
                
                if not resources:
                    self.log("未找到VISA仪器")
                    self.log("提示: 确保仪器已连接并安装了正确的驱动")
                    
            except Exception as e:
                self.log(f"扫描错误: {e}")
        else:
            # 模拟模式
            mock_resources = [
                "USB0::0x1AB1::0x0588::DS1ZA123456789::INSTR",
                "TCPIP0::192.168.1.100::INSTR",
                "GPIB0::1::INSTR",
                "ASRL3::INSTR"
            ]
            for res in mock_resources:
                self.list_resources.addItem(res + " (模拟)")
            self.log("模拟模式: 添加虚拟仪器")
    
    def connect_instrument(self):
        """连接仪器"""
        item = self.list_resources.currentItem()
        if not item:
            QMessageBox.warning(self, "警告", "请先选择一个仪器")
            return
        
        resource = item.text().replace(" (模拟)", "")
        
        if VISA_AVAILABLE and self.rm:
            try:
                self.instrument = self.rm.open_resource(resource)
                self.instrument.timeout = self.spin_timeout.value()
                
                # 查询IDN
                try:
                    idn = self.instrument.query('*IDN?').strip()
                    self.label_idn.setText(idn)
                    self.log(f"IDN: {idn}")
                except Exception:
                    self.label_idn.setText("(无法获取)")
                
                self.update_connection_state(True, resource)
                self.log(f"已连接: {resource}")
                
            except Exception as e:
                self.log(f"连接失败: {e}")
        else:
            # 模拟模式
            class MockInstrument:
                def query(self, cmd):
                    if '*IDN?' in cmd:
                        return "Simulated Instrument, Model 1234, SN:ABC123, Ver1.0"
                    return f"Response to: {cmd}"
                def write(self, cmd): pass
                def close(self): pass
            
            self.instrument = MockInstrument()
            self.label_idn.setText("Simulated Instrument")
            self.update_connection_state(True, resource)
            self.log(f"[模拟] 已连接: {resource}")
    
    def disconnect_instrument(self):
        """断开仪器"""
        if self.instrument:
            try:
                self.instrument.close()
            except Exception:
                pass
            self.instrument = None
        
        self.label_idn.setText("-")
        self.update_connection_state(False)
        self.log("已断开连接")
    
    def update_connection_state(self, connected: bool, resource: str = ""):
        """更新连接状态"""
        self.btn_connect.setEnabled(not connected)
        self.btn_disconnect.setEnabled(connected)
        self.btn_send.setEnabled(connected)
        self.btn_query.setEnabled(connected)
        
        if connected:
            self.label_status.setText(f"● 已连接")
            self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.label_status.setText("● 未连接")
            self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def send_command(self):
        """发送命令（不等待响应）"""
        if not self.instrument:
            return
        
        cmd = self.line_command.text().strip()
        if not cmd:
            return
        
        try:
            self.instrument.write(cmd)
            self.log(f"→ {cmd}")
        except Exception as e:
            self.log(f"发送错误: {e}")
    
    def query_command(self):
        """查询命令（等待响应）"""
        if not self.instrument:
            return
        
        cmd = self.line_command.text().strip()
        if not cmd:
            return
        
        try:
            response = self.instrument.query(cmd).strip()
            self.log(f"→ {cmd}")
            self.log(f"← {response}")
        except Exception as e:
            self.log(f"查询错误: {e}")
    
    def quick_query(self, cmd: str):
        """快捷查询"""
        if not self.instrument:
            self.log("请先连接仪器")
            return
        
        try:
            if cmd.endswith('?'):
                response = self.instrument.query(cmd).strip()
                self.log(f"→ {cmd}")
                self.log(f"← {response}")
            else:
                self.instrument.write(cmd)
                self.log(f"→ {cmd}")
        except Exception as e:
            self.log(f"命令错误: {e}")
    
    def log(self, message: str):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.append(f"[{time_str}] {message}")
    
    def closeEvent(self, event):
        """关闭窗口"""
        if self.instrument:
            try:
                self.instrument.close()
            except Exception:
                pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = VisaControlDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

