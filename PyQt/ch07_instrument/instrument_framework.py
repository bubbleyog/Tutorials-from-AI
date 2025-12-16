"""
示例程序：完整仪器控制框架
所属章节：第七章 - 仪器控制界面实战

功能说明：
    演示可扩展的仪器控制框架：
    - 仪器抽象基类
    - 串口/网络仪器实现
    - 控制器与GUI分离
    - 仪器管理器

运行方式：
    python instrument_framework.py
"""

import sys
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QGroupBox, QFormLayout,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QSpinBox, QTabWidget, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer, QObject, pyqtSignal


# ============================================================
# 仪器状态枚举
# ============================================================

class InstrumentState(Enum):
    """仪器状态"""
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    ERROR = 3


# ============================================================
# 仪器抽象基类
# ============================================================

class InstrumentBase(ABC):
    """
    仪器抽象基类
    
    所有仪器驱动都应继承此类并实现抽象方法
    """
    
    def __init__(self, name: str = "Unknown"):
        self.name = name
        self._state = InstrumentState.DISCONNECTED
        self._last_error = ""
    
    @property
    def state(self) -> InstrumentState:
        return self._state
    
    @property
    def last_error(self) -> str:
        return self._last_error
    
    @property
    def is_connected(self) -> bool:
        return self._state == InstrumentState.CONNECTED
    
    @abstractmethod
    def connect(self) -> bool:
        """连接仪器"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def query(self, command: str) -> str:
        """发送查询命令并返回响应"""
        pass
    
    @abstractmethod
    def write(self, command: str):
        """发送写命令"""
        pass
    
    def get_idn(self) -> str:
        """获取仪器ID"""
        try:
            return self.query("*IDN?")
        except Exception:
            return "Unknown"


# ============================================================
# 模拟仪器实现
# ============================================================

class SimulatedInstrument(InstrumentBase):
    """
    模拟仪器（用于测试和演示）
    """
    
    def __init__(self, name: str = "Simulated Instrument"):
        super().__init__(name)
        self.idn = f"Simulated,{name},SN123456,V1.0"
        self._values = {
            'VOLT': 0.0,
            'CURR': 0.0,
            'TEMP': 300.0,
            'FREQ': 1000.0,
            'OUTP': 'OFF'
        }
    
    def connect(self) -> bool:
        self._state = InstrumentState.CONNECTING
        time.sleep(0.1)  # 模拟连接延迟
        self._state = InstrumentState.CONNECTED
        return True
    
    def disconnect(self):
        self._state = InstrumentState.DISCONNECTED
    
    def query(self, command: str) -> str:
        if not self.is_connected:
            raise Exception("仪器未连接")
        
        cmd = command.strip().upper()
        
        if cmd == "*IDN?":
            return self.idn
        elif cmd == ":VOLT?":
            return f"{self._values['VOLT']:.4f}"
        elif cmd == ":CURR?":
            return f"{self._values['CURR']:.6f}"
        elif cmd == ":TEMP?":
            # 添加一些随机波动
            import random
            self._values['TEMP'] += random.uniform(-0.1, 0.1)
            return f"{self._values['TEMP']:.2f}"
        elif cmd == ":FREQ?":
            return f"{self._values['FREQ']:.1f}"
        elif cmd == ":OUTP?":
            return self._values['OUTP']
        elif cmd == ":SYST:ERR?":
            return "0,No error"
        else:
            return f"Response to: {command}"
    
    def write(self, command: str):
        if not self.is_connected:
            raise Exception("仪器未连接")
        
        cmd = command.strip().upper()
        
        if cmd.startswith(":VOLT "):
            self._values['VOLT'] = float(cmd.split()[1])
        elif cmd.startswith(":CURR "):
            self._values['CURR'] = float(cmd.split()[1])
        elif cmd.startswith(":FREQ "):
            self._values['FREQ'] = float(cmd.split()[1])
        elif cmd == ":OUTP ON":
            self._values['OUTP'] = 'ON'
        elif cmd == ":OUTP OFF":
            self._values['OUTP'] = 'OFF'


class SimulatedPowerSupply(SimulatedInstrument):
    """模拟电源"""
    
    def __init__(self):
        super().__init__("Power Supply")
        self.idn = "Simulated,PSU-3000,SN-PSU-001,V2.0"
        self._values = {
            'VOLT': 0.0,
            'CURR': 0.0,
            'VOLT:LIM': 30.0,
            'CURR:LIM': 3.0,
            'OUTP': 'OFF'
        }


class SimulatedMultimeter(SimulatedInstrument):
    """模拟万用表"""
    
    def __init__(self):
        super().__init__("Multimeter")
        self.idn = "Simulated,DMM-6500,SN-DMM-001,V1.5"
    
    def query(self, command: str) -> str:
        cmd = command.strip().upper()
        
        if cmd == ":MEAS:VOLT:DC?":
            import random
            return f"{random.uniform(0, 10):.6f}"
        elif cmd == ":MEAS:CURR:DC?":
            import random
            return f"{random.uniform(0, 0.1):.8f}"
        elif cmd == ":MEAS:RES?":
            import random
            return f"{random.uniform(100, 10000):.2f}"
        
        return super().query(command)


# ============================================================
# 仪器控制器
# ============================================================

class InstrumentController(QObject):
    """
    仪器控制器
    
    作为GUI和仪器之间的中间层，处理业务逻辑
    """
    
    # 信号定义
    connected = pyqtSignal(str)
    disconnected = pyqtSignal()
    data_received = pyqtSignal(dict)
    error = pyqtSignal(str)
    state_changed = pyqtSignal(InstrumentState)
    
    def __init__(self, instrument: InstrumentBase):
        super().__init__()
        self.instrument = instrument
        
        # 轮询定时器
        self.polling_timer = QTimer()
        self.polling_timer.timeout.connect(self.poll_data)
        self.polling_interval = 1000  # ms
        
        # 要轮询的参数
        self.poll_commands = []
    
    def connect_instrument(self) -> bool:
        """连接仪器"""
        try:
            if self.instrument.connect():
                idn = self.instrument.get_idn()
                self.connected.emit(idn)
                self.state_changed.emit(InstrumentState.CONNECTED)
                return True
        except Exception as e:
            self.error.emit(str(e))
        
        self.state_changed.emit(InstrumentState.ERROR)
        return False
    
    def disconnect_instrument(self):
        """断开仪器"""
        self.stop_polling()
        self.instrument.disconnect()
        self.disconnected.emit()
        self.state_changed.emit(InstrumentState.DISCONNECTED)
    
    def start_polling(self, commands: List[str] = None, interval: int = 1000):
        """开始轮询"""
        if commands:
            self.poll_commands = commands
        self.polling_interval = interval
        self.polling_timer.start(interval)
    
    def stop_polling(self):
        """停止轮询"""
        self.polling_timer.stop()
    
    def poll_data(self):
        """轮询数据"""
        if not self.instrument.is_connected:
            return
        
        data = {}
        try:
            for cmd in self.poll_commands:
                response = self.instrument.query(cmd)
                # 解析命令名作为键
                key = cmd.replace(':', '').replace('?', '')
                data[key] = response
            
            self.data_received.emit(data)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def send_command(self, command: str) -> Optional[str]:
        """发送命令"""
        try:
            if command.strip().endswith('?'):
                return self.instrument.query(command)
            else:
                self.instrument.write(command)
                return None
        except Exception as e:
            self.error.emit(str(e))
            return None


# ============================================================
# 仪器管理器
# ============================================================

class InstrumentManager:
    """
    仪器管理器
    
    管理多个仪器的注册和访问
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._instruments = {}
        return cls._instance
    
    def register(self, name: str, instrument: InstrumentBase):
        """注册仪器"""
        self._instruments[name] = instrument
    
    def get(self, name: str) -> Optional[InstrumentBase]:
        """获取仪器"""
        return self._instruments.get(name)
    
    def list_instruments(self) -> List[str]:
        """列出所有仪器"""
        return list(self._instruments.keys())
    
    def remove(self, name: str):
        """移除仪器"""
        if name in self._instruments:
            del self._instruments[name]


# ============================================================
# GUI 界面
# ============================================================

class InstrumentFrameworkDemo(QMainWindow):
    """仪器控制框架演示"""
    
    def __init__(self):
        super().__init__()
        
        # 创建仪器管理器
        self.manager = InstrumentManager()
        
        # 注册模拟仪器
        self.manager.register("PSU", SimulatedPowerSupply())
        self.manager.register("DMM", SimulatedMultimeter())
        self.manager.register("TEMP", SimulatedInstrument("Temperature Controller"))
        
        # 控制器字典
        self.controllers: Dict[str, InstrumentController] = {}
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("仪器控制框架")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：仪器列表
        left_panel = QWidget()
        left_panel.setFixedWidth(280)
        left_layout = QVBoxLayout(left_panel)
        
        # 仪器列表
        list_group = QGroupBox("仪器列表")
        list_layout = QVBoxLayout()
        
        self.instrument_table = QTableWidget(0, 3)
        self.instrument_table.setHorizontalHeaderLabels(['名称', '类型', '状态'])
        self.instrument_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.instrument_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.instrument_table.itemSelectionChanged.connect(self.on_instrument_selected)
        list_layout.addWidget(self.instrument_table)
        
        self.refresh_instrument_list()
        
        btn_refresh = QPushButton("🔄 刷新列表")
        btn_refresh.clicked.connect(self.refresh_instrument_list)
        list_layout.addWidget(btn_refresh)
        
        list_group.setLayout(list_layout)
        left_layout.addWidget(list_group)
        
        # 连接控制
        conn_group = QGroupBox("连接控制")
        conn_layout = QVBoxLayout()
        
        self.btn_connect = QPushButton("🔌 连接")
        self.btn_connect.clicked.connect(self.connect_selected)
        conn_layout.addWidget(self.btn_connect)
        
        self.btn_disconnect = QPushButton("⏏️ 断开")
        self.btn_disconnect.clicked.connect(self.disconnect_selected)
        conn_layout.addWidget(self.btn_disconnect)
        
        conn_group.setLayout(conn_layout)
        left_layout.addWidget(conn_group)
        
        left_layout.addStretch()
        
        main_layout.addWidget(left_panel)
        
        # 右侧：控制面板
        right_layout = QVBoxLayout()
        
        # 仪器信息
        info_group = QGroupBox("仪器信息")
        info_layout = QFormLayout()
        
        self.label_name = QLabel("-")
        info_layout.addRow("名称:", self.label_name)
        
        self.label_idn = QLabel("-")
        self.label_idn.setWordWrap(True)
        info_layout.addRow("IDN:", self.label_idn)
        
        self.label_state = QLabel("未连接")
        self.label_state.setStyleSheet("color: #e74c3c;")
        info_layout.addRow("状态:", self.label_state)
        
        info_group.setLayout(info_layout)
        right_layout.addWidget(info_group)
        
        # 命令发送
        cmd_group = QGroupBox("命令发送")
        cmd_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        self.line_command = QLineEdit()
        self.line_command.setPlaceholderText("输入SCPI命令...")
        self.line_command.returnPressed.connect(self.send_command)
        input_layout.addWidget(self.line_command)
        
        btn_send = QPushButton("发送")
        btn_send.clicked.connect(self.send_command)
        input_layout.addWidget(btn_send)
        
        cmd_layout.addLayout(input_layout)
        
        # 快捷命令
        quick_layout = QHBoxLayout()
        for cmd in ['*IDN?', ':VOLT?', ':CURR?', ':TEMP?', ':OUTP?']:
            btn = QPushButton(cmd)
            btn.clicked.connect(lambda c, cmd=cmd: self.quick_command(cmd))
            quick_layout.addWidget(btn)
        cmd_layout.addLayout(quick_layout)
        
        cmd_group.setLayout(cmd_layout)
        right_layout.addWidget(cmd_group)
        
        # 实时数据
        data_group = QGroupBox("实时数据")
        data_layout = QVBoxLayout()
        
        polling_layout = QHBoxLayout()
        self.check_polling = QCheckBox("启用轮询")
        self.check_polling.stateChanged.connect(self.toggle_polling)
        polling_layout.addWidget(self.check_polling)
        
        polling_layout.addWidget(QLabel("间隔:"))
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(100, 10000)
        self.spin_interval.setValue(1000)
        self.spin_interval.setSuffix(" ms")
        polling_layout.addWidget(self.spin_interval)
        polling_layout.addStretch()
        data_layout.addLayout(polling_layout)
        
        self.data_table = QTableWidget(5, 2)
        self.data_table.setHorizontalHeaderLabels(['参数', '值'])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        data_layout.addWidget(self.data_table)
        
        data_group.setLayout(data_layout)
        right_layout.addWidget(data_group)
        
        # 日志
        log_group = QGroupBox("通信日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        right_layout.addWidget(log_group)
        
        main_layout.addLayout(right_layout)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #ecf0f1; }
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
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QLineEdit, QSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTableWidget {
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
            }
        """)
        
        self.current_instrument_name = None
    
    def refresh_instrument_list(self):
        """刷新仪器列表"""
        self.instrument_table.setRowCount(0)
        
        for name in self.manager.list_instruments():
            instrument = self.manager.get(name)
            row = self.instrument_table.rowCount()
            self.instrument_table.insertRow(row)
            
            self.instrument_table.setItem(row, 0, QTableWidgetItem(name))
            self.instrument_table.setItem(row, 1, QTableWidgetItem(instrument.name))
            
            state_item = QTableWidgetItem(instrument.state.name)
            if instrument.state == InstrumentState.CONNECTED:
                state_item.setForeground(Qt.GlobalColor.darkGreen)
            elif instrument.state == InstrumentState.ERROR:
                state_item.setForeground(Qt.GlobalColor.red)
            self.instrument_table.setItem(row, 2, state_item)
    
    def on_instrument_selected(self):
        """选择仪器"""
        selected = self.instrument_table.selectedItems()
        if not selected:
            return
        
        row = selected[0].row()
        name = self.instrument_table.item(row, 0).text()
        self.current_instrument_name = name
        
        instrument = self.manager.get(name)
        self.label_name.setText(name)
        
        if instrument.is_connected:
            self.label_idn.setText(instrument.get_idn())
            self.label_state.setText("已连接")
            self.label_state.setStyleSheet("color: #27ae60;")
        else:
            self.label_idn.setText("-")
            self.label_state.setText("未连接")
            self.label_state.setStyleSheet("color: #e74c3c;")
    
    def get_current_controller(self) -> Optional[InstrumentController]:
        """获取当前控制器"""
        if not self.current_instrument_name:
            return None
        
        if self.current_instrument_name not in self.controllers:
            instrument = self.manager.get(self.current_instrument_name)
            if instrument:
                controller = InstrumentController(instrument)
                controller.connected.connect(self.on_connected)
                controller.disconnected.connect(self.on_disconnected)
                controller.data_received.connect(self.on_data_received)
                controller.error.connect(self.on_error)
                self.controllers[self.current_instrument_name] = controller
        
        return self.controllers.get(self.current_instrument_name)
    
    def connect_selected(self):
        """连接选中仪器"""
        controller = self.get_current_controller()
        if controller:
            self.log(f"正在连接 {self.current_instrument_name}...")
            if controller.connect_instrument():
                self.log("连接成功")
            else:
                self.log("连接失败")
            self.refresh_instrument_list()
            self.on_instrument_selected()
    
    def disconnect_selected(self):
        """断开选中仪器"""
        controller = self.get_current_controller()
        if controller:
            controller.disconnect_instrument()
            self.log(f"已断开 {self.current_instrument_name}")
            self.check_polling.setChecked(False)
            self.refresh_instrument_list()
            self.on_instrument_selected()
    
    def send_command(self):
        """发送命令"""
        controller = self.get_current_controller()
        if not controller or not controller.instrument.is_connected:
            QMessageBox.warning(self, "警告", "请先连接仪器")
            return
        
        cmd = self.line_command.text().strip()
        if not cmd:
            return
        
        self.log(f"→ {cmd}")
        response = controller.send_command(cmd)
        if response is not None:
            self.log(f"← {response}")
        
        self.line_command.clear()
    
    def quick_command(self, cmd: str):
        """快捷命令"""
        self.line_command.setText(cmd)
        self.send_command()
    
    def toggle_polling(self, state: int):
        """切换轮询"""
        controller = self.get_current_controller()
        if not controller:
            return
        
        if state == Qt.CheckState.Checked.value:
            if not controller.instrument.is_connected:
                QMessageBox.warning(self, "警告", "请先连接仪器")
                self.check_polling.setChecked(False)
                return
            
            commands = [':VOLT?', ':CURR?', ':TEMP?', ':OUTP?']
            interval = self.spin_interval.value()
            controller.start_polling(commands, interval)
            self.log(f"开始轮询，间隔 {interval}ms")
        else:
            controller.stop_polling()
            self.log("停止轮询")
    
    def on_connected(self, idn: str):
        """连接成功"""
        self.label_idn.setText(idn)
        self.label_state.setText("已连接")
        self.label_state.setStyleSheet("color: #27ae60;")
    
    def on_disconnected(self):
        """断开连接"""
        self.label_idn.setText("-")
        self.label_state.setText("未连接")
        self.label_state.setStyleSheet("color: #e74c3c;")
    
    def on_data_received(self, data: dict):
        """接收数据"""
        self.data_table.setRowCount(len(data))
        for i, (key, value) in enumerate(data.items()):
            self.data_table.setItem(i, 0, QTableWidgetItem(key))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(value)))
    
    def on_error(self, error: str):
        """错误处理"""
        self.log(f"错误: {error}")
    
    def log(self, message: str):
        """添加日志"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")
    
    def closeEvent(self, event):
        """关闭窗口"""
        for controller in self.controllers.values():
            controller.stop_polling()
            if controller.instrument.is_connected:
                controller.instrument.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = InstrumentFrameworkDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

