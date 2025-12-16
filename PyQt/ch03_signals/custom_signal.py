"""
示例程序：自定义信号
所属章节：第三章 - 信号与槽机制

功能说明：
    演示如何创建和使用自定义信号，包括：
    - 定义无参数信号
    - 定义带参数信号
    - 发出信号
    - 物理实验场景：温度监控系统

运行方式：
    python custom_signal.py
"""

import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QDoubleSpinBox, QProgressBar, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, QObject, QTimer, pyqtSignal


# ============================================================
# 自定义信号示例1：简单的数据处理器
# ============================================================

class DataProcessor(QObject):
    """
    数据处理器类
    
    演示自定义信号的定义和发出
    """
    
    # 定义自定义信号（必须作为类属性）
    started = pyqtSignal()                    # 无参数信号
    progress = pyqtSignal(int)                # int参数：进度百分比
    data_ready = pyqtSignal(list)             # list参数：处理后的数据
    finished = pyqtSignal(str, float)         # 多参数：状态消息和耗时
    error = pyqtSignal(str)                   # str参数：错误信息
    
    def __init__(self):
        super().__init__()
        self._is_running = False
    
    def process(self, data: list):
        """处理数据并发出信号"""
        self._is_running = True
        
        # 发出开始信号
        self.started.emit()
        
        try:
            result = []
            total = len(data)
            
            for i, item in enumerate(data):
                # 模拟处理
                result.append(item * 2)
                
                # 发出进度信号
                progress_percent = int((i + 1) / total * 100)
                self.progress.emit(progress_percent)
            
            # 发出数据就绪信号
            self.data_ready.emit(result)
            
            # 发出完成信号
            self.finished.emit("处理成功", 1.5)
            
        except Exception as e:
            # 发出错误信号
            self.error.emit(str(e))
        
        finally:
            self._is_running = False


# ============================================================
# 自定义信号示例2：温度监控系统（物理实验场景）
# ============================================================

class TemperatureController(QObject):
    """
    温度控制器
    
    模拟低温物理实验中的温度监控系统
    """
    
    # 定义信号
    temperature_changed = pyqtSignal(float)           # 温度变化
    target_reached = pyqtSignal(float)                # 到达目标温度
    stability_changed = pyqtSignal(bool, float)       # 稳定性变化(是否稳定, 波动值)
    alarm = pyqtSignal(str, float)                    # 报警(原因, 当前温度)
    status_update = pyqtSignal(dict)                  # 状态更新(完整状态字典)
    
    def __init__(self):
        super().__init__()
        self._current_temp = 300.0      # 当前温度 (K)
        self._target_temp = 300.0       # 目标温度 (K)
        self._min_temp = 1.5            # 最低温度限制
        self._max_temp = 400.0          # 最高温度限制
        self._fluctuation = 0.0         # 温度波动
        self._is_stable = False
        
        # 模拟温度变化的定时器
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_temperature)
    
    def start(self):
        """启动温度控制"""
        self._timer.start(500)  # 每500ms更新一次
    
    def stop(self):
        """停止温度控制"""
        self._timer.stop()
    
    def set_target(self, target: float):
        """设置目标温度"""
        if self._min_temp <= target <= self._max_temp:
            self._target_temp = target
        else:
            self.alarm.emit("目标温度超出范围", target)
    
    def _update_temperature(self):
        """更新温度（模拟）"""
        # 模拟温度向目标靠近
        diff = self._target_temp - self._current_temp
        
        if abs(diff) > 1.0:
            # 大温差：快速变化
            change = diff * 0.1 + random.uniform(-0.5, 0.5)
            self._is_stable = False
        else:
            # 接近目标：小波动
            change = diff * 0.3 + random.uniform(-0.2, 0.2)
            
            # 检查是否稳定
            if abs(diff) < 0.5:
                if not self._is_stable:
                    self._is_stable = True
                    self.target_reached.emit(self._current_temp)
        
        self._current_temp += change
        self._fluctuation = abs(change)
        
        # 发出温度变化信号
        self.temperature_changed.emit(self._current_temp)
        
        # 发出稳定性信号
        self.stability_changed.emit(self._is_stable, self._fluctuation)
        
        # 发出状态更新信号
        self.status_update.emit({
            "current": self._current_temp,
            "target": self._target_temp,
            "stable": self._is_stable,
            "fluctuation": self._fluctuation
        })
        
        # 检查报警条件
        if self._current_temp > 350:
            self.alarm.emit("温度过高警告", self._current_temp)
        elif self._current_temp < 10:
            self.alarm.emit("接近极低温", self._current_temp)


# ============================================================
# GUI界面
# ============================================================

class TemperatureMonitorUI(QMainWindow):
    """温度监控界面"""
    
    def __init__(self):
        super().__init__()
        self.controller = TemperatureController()
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        self.setWindowTitle("温度控制系统 - 自定义信号演示")
        self.setMinimumSize(600, 500)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        
        # 标题
        title = QLabel("🌡 低温实验温度监控系统")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 温度显示
        main_layout.addWidget(self.create_display_group())
        
        # 控制面板
        main_layout.addWidget(self.create_control_group())
        
        # 日志
        main_layout.addWidget(self.create_log_group())
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QLabel { color: #ecf0f1; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
            QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #5d6d7e;
                border-radius: 5px;
                background-color: #1a252f;
                color: #ecf0f1;
                font-size: 14px;
            }
        """)
    
    def create_display_group(self) -> QGroupBox:
        """创建温度显示区"""
        group = QGroupBox("实时温度")
        layout = QGridLayout()
        
        # 当前温度（大字体显示）
        self.label_current = QLabel("300.00 K")
        self.label_current.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #3498db;
            font-family: 'Consolas', monospace;
        """)
        self.label_current.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_current, 0, 0, 1, 2)
        
        # 目标温度
        layout.addWidget(QLabel("目标温度:"), 1, 0)
        self.label_target = QLabel("300.00 K")
        self.label_target.setStyleSheet("color: #f39c12; font-size: 16px;")
        layout.addWidget(self.label_target, 1, 1)
        
        # 稳定性
        layout.addWidget(QLabel("状态:"), 2, 0)
        self.label_status = QLabel("● 变化中")
        self.label_status.setStyleSheet("color: #e74c3c; font-size: 14px;")
        layout.addWidget(self.label_status, 2, 1)
        
        # 波动值
        layout.addWidget(QLabel("波动:"), 3, 0)
        self.label_fluctuation = QLabel("0.00 K")
        self.label_fluctuation.setStyleSheet("color: #95a5a6; font-size: 14px;")
        layout.addWidget(self.label_fluctuation, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def create_control_group(self) -> QGroupBox:
        """创建控制面板"""
        group = QGroupBox("控制面板")
        layout = QHBoxLayout()
        
        # 目标温度设置
        layout.addWidget(QLabel("设置目标:"))
        self.spin_target = QDoubleSpinBox()
        self.spin_target.setRange(1.5, 400)
        self.spin_target.setValue(300)
        self.spin_target.setSuffix(" K")
        self.spin_target.setDecimals(1)
        layout.addWidget(self.spin_target)
        
        # 应用按钮
        self.btn_apply = QPushButton("应用")
        self.btn_apply.setStyleSheet("background-color: #3498db;")
        self.btn_apply.clicked.connect(self.apply_target)
        layout.addWidget(self.btn_apply)
        
        layout.addStretch()
        
        # 启动/停止按钮
        self.btn_start = QPushButton("▶ 启动")
        self.btn_start.setStyleSheet("background-color: #27ae60;")
        self.btn_start.clicked.connect(self.toggle_control)
        layout.addWidget(self.btn_start)
        
        # 快捷温度按钮
        for temp, name in [(4.2, "液氦"), (77, "液氮"), (300, "室温")]:
            btn = QPushButton(f"{name}\n{temp}K")
            btn.setStyleSheet("background-color: #5d6d7e; font-size: 11px;")
            btn.clicked.connect(lambda _, t=temp: self.set_quick_target(t))
            layout.addWidget(btn)
        
        group.setLayout(layout)
        return group
    
    def create_log_group(self) -> QGroupBox:
        """创建日志区"""
        group = QGroupBox("事件日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2e;
                color: #00ff88;
                font-family: Consolas, monospace;
                border: none;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def connect_signals(self):
        """连接自定义信号到槽函数"""
        # 温度变化信号
        self.controller.temperature_changed.connect(self.on_temperature_changed)
        
        # 到达目标信号
        self.controller.target_reached.connect(self.on_target_reached)
        
        # 稳定性变化信号
        self.controller.stability_changed.connect(self.on_stability_changed)
        
        # 报警信号
        self.controller.alarm.connect(self.on_alarm)
        
        # 状态更新信号（用于完整状态）
        self.controller.status_update.connect(self.on_status_update)
    
    # ========== 槽函数 ==========
    
    def on_temperature_changed(self, temp: float):
        """温度变化槽"""
        self.label_current.setText(f"{temp:.2f} K")
        
        # 根据温度改变颜色
        if temp < 50:
            color = "#3498db"  # 蓝色（低温）
        elif temp < 200:
            color = "#27ae60"  # 绿色（中等）
        else:
            color = "#e74c3c"  # 红色（高温）
        
        self.label_current.setStyleSheet(f"""
            font-size: 48px;
            font-weight: bold;
            color: {color};
            font-family: 'Consolas', monospace;
        """)
    
    def on_target_reached(self, temp: float):
        """到达目标温度槽"""
        self.log(f"✓ 到达目标温度: {temp:.2f} K")
    
    def on_stability_changed(self, is_stable: bool, fluctuation: float):
        """稳定性变化槽"""
        if is_stable:
            self.label_status.setText("● 稳定")
            self.label_status.setStyleSheet("color: #27ae60; font-size: 14px;")
        else:
            self.label_status.setText("● 变化中")
            self.label_status.setStyleSheet("color: #e74c3c; font-size: 14px;")
        
        self.label_fluctuation.setText(f"{fluctuation:.3f} K")
    
    def on_alarm(self, reason: str, temp: float):
        """报警槽"""
        self.log(f"⚠ 警告: {reason} (当前: {temp:.2f} K)")
    
    def on_status_update(self, status: dict):
        """状态更新槽（接收字典）"""
        # 可以在这里处理完整状态
        pass
    
    # ========== 控制函数 ==========
    
    def apply_target(self):
        """应用目标温度"""
        target = self.spin_target.value()
        self.controller.set_target(target)
        self.label_target.setText(f"{target:.2f} K")
        self.log(f"设置目标温度: {target:.1f} K")
    
    def set_quick_target(self, temp: float):
        """快捷设置温度"""
        self.spin_target.setValue(temp)
        self.apply_target()
    
    def toggle_control(self):
        """切换控制状态"""
        if self.btn_start.text().startswith("▶"):
            self.controller.start()
            self.btn_start.setText("⏹ 停止")
            self.btn_start.setStyleSheet("background-color: #e74c3c;")
            self.log("温度控制已启动")
        else:
            self.controller.stop()
            self.btn_start.setText("▶ 启动")
            self.btn_start.setStyleSheet("background-color: #27ae60;")
            self.log("温度控制已停止")
    
    def log(self, message: str):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")
    
    def closeEvent(self, event):
        """窗口关闭时停止控制器"""
        self.controller.stop()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = TemperatureMonitorUI()
    window.show()
    
    # 打印信号说明
    print("=" * 50)
    print("自定义信号演示 - 温度控制系统")
    print("=" * 50)
    print("定义的信号:")
    print("  - temperature_changed(float): 温度变化")
    print("  - target_reached(float): 到达目标温度")
    print("  - stability_changed(bool, float): 稳定性变化")
    print("  - alarm(str, float): 报警")
    print("  - status_update(dict): 状态更新")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

