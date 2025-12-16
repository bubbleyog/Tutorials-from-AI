"""
示例程序：日志系统
所属章节：第八章 - 项目实战与部署

功能说明：
    演示完整的日志系统：
    - 多级别日志
    - 文件轮转
    - GUI日志查看器
    - 实时日志显示

运行方式：
    python logging_system.py
"""

import sys
import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QGroupBox, QFormLayout,
    QComboBox, QTextEdit, QSpinBox, QCheckBox, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QTextCharFormat, QFont


# ============================================================
# 日志处理器
# ============================================================

class QTextEditHandler(logging.Handler):
    """
    将日志输出到QTextEdit的处理器
    """
    
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        
        # 级别颜色
        self.colors = {
            logging.DEBUG: '#95a5a6',
            logging.INFO: '#27ae60',
            logging.WARNING: '#f39c12',
            logging.ERROR: '#e74c3c',
            logging.CRITICAL: '#c0392b'
        }
    
    def emit(self, record):
        try:
            msg = self.format(record)
            color = self.colors.get(record.levelno, '#ecf0f1')
            html = f'<span style="color: {color}">{msg}</span>'
            self.text_edit.append(html)
        except Exception:
            self.handleError(record)


class SignalHandler(logging.Handler, QObject):
    """
    发送信号的日志处理器
    """
    
    log_signal = pyqtSignal(str, int)
    
    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)
    
    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_signal.emit(msg, record.levelno)
        except Exception:
            self.handleError(record)


# ============================================================
# 日志管理器
# ============================================================

class LogManager:
    """
    日志管理器
    
    提供统一的日志配置和管理
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def setup(self, 
              log_file: str = None,
              level: str = "INFO",
              max_bytes: int = 10*1024*1024,
              backup_count: int = 5,
              console: bool = True) -> logging.Logger:
        """
        配置日志系统
        
        Args:
            log_file: 日志文件路径
            level: 日志级别
            max_bytes: 单个日志文件最大大小
            backup_count: 保留的备份文件数量
            console: 是否输出到控制台
        """
        if self._initialized:
            return logging.getLogger()
        
        # 创建根logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, level.upper()))
        
        # 清除已有处理器
        logger.handlers.clear()
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        self._initialized = True
        return logger
    
    def add_gui_handler(self, text_edit: QTextEdit):
        """添加GUI处理器"""
        logger = logging.getLogger()
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        handler = QTextEditHandler(text_edit)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return handler
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """获取logger"""
        return logging.getLogger(name)


# ============================================================
# 日志查看器GUI
# ============================================================

class LogViewerDemo(QMainWindow):
    """日志系统演示"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化日志管理器
        self.log_manager = LogManager()
        self.log_manager.setup(
            log_file="./logs/demo.log",
            level="DEBUG",
            console=True
        )
        
        self.logger = self.log_manager.get_logger(__name__)
        
        self.init_ui()
        
        # 添加GUI处理器
        self.log_manager.add_gui_handler(self.log_text)
        
        self.logger.info("日志系统已启动")
    
    def init_ui(self):
        self.setWindowTitle("日志系统")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # 发送日志
        send_group = QGroupBox("发送日志")
        send_layout = QVBoxLayout()
        
        self.line_message = QLineEdit()
        self.line_message.setPlaceholderText("输入日志消息...")
        self.line_message.returnPressed.connect(lambda: self.send_log("INFO"))
        send_layout.addWidget(self.line_message)
        
        level_layout = QHBoxLayout()
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            btn = QPushButton(level)
            btn.clicked.connect(lambda c, l=level: self.send_log(l))
            
            # 设置按钮颜色
            colors = {
                'DEBUG': '#95a5a6',
                'INFO': '#27ae60',
                'WARNING': '#f39c12',
                'ERROR': '#e74c3c',
                'CRITICAL': '#c0392b'
            }
            btn.setStyleSheet(f"background-color: {colors[level]};")
            level_layout.addWidget(btn)
        
        send_layout.addLayout(level_layout)
        send_group.setLayout(send_layout)
        left_layout.addWidget(send_group)
        
        # 模拟日志
        sim_group = QGroupBox("模拟日志")
        sim_layout = QVBoxLayout()
        
        self.check_auto_log = QCheckBox("自动生成日志")
        self.check_auto_log.stateChanged.connect(self.toggle_auto_log)
        sim_layout.addWidget(self.check_auto_log)
        
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("间隔:"))
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(100, 5000)
        self.spin_interval.setValue(1000)
        self.spin_interval.setSuffix(" ms")
        interval_layout.addWidget(self.spin_interval)
        sim_layout.addLayout(interval_layout)
        
        btn_sim_error = QPushButton("模拟异常")
        btn_sim_error.clicked.connect(self.simulate_error)
        sim_layout.addWidget(btn_sim_error)
        
        sim_group.setLayout(sim_layout)
        left_layout.addWidget(sim_group)
        
        # 日志配置
        config_group = QGroupBox("日志配置")
        config_layout = QFormLayout()
        
        self.combo_level = QComboBox()
        self.combo_level.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        self.combo_level.setCurrentText('DEBUG')
        self.combo_level.currentTextChanged.connect(self.change_level)
        config_layout.addRow("级别:", self.combo_level)
        
        self.spin_max_lines = QSpinBox()
        self.spin_max_lines.setRange(100, 10000)
        self.spin_max_lines.setValue(1000)
        config_layout.addRow("最大行数:", self.spin_max_lines)
        
        config_group.setLayout(config_layout)
        left_layout.addWidget(config_group)
        
        # 文件操作
        file_group = QGroupBox("日志文件")
        file_layout = QVBoxLayout()
        
        btn_open_log = QPushButton("📂 打开日志文件")
        btn_open_log.clicked.connect(self.open_log_file)
        file_layout.addWidget(btn_open_log)
        
        btn_open_folder = QPushButton("📁 打开日志目录")
        btn_open_folder.clicked.connect(self.open_log_folder)
        file_layout.addWidget(btn_open_folder)
        
        btn_export = QPushButton("💾 导出日志")
        btn_export.clicked.connect(self.export_log)
        file_layout.addWidget(btn_export)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        left_layout.addStretch()
        
        # 清空按钮
        btn_clear = QPushButton("🗑️ 清空日志")
        btn_clear.clicked.connect(lambda: self.log_text.clear())
        left_layout.addWidget(btn_clear)
        
        splitter.addWidget(left_panel)
        
        # 右侧日志显示
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 过滤器
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("过滤:"))
        
        self.line_filter = QLineEdit()
        self.line_filter.setPlaceholderText("输入关键词过滤...")
        self.line_filter.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.line_filter)
        
        self.check_debug = QCheckBox("DEBUG")
        self.check_debug.setChecked(True)
        filter_layout.addWidget(self.check_debug)
        
        self.check_info = QCheckBox("INFO")
        self.check_info.setChecked(True)
        filter_layout.addWidget(self.check_info)
        
        self.check_warning = QCheckBox("WARNING")
        self.check_warning.setChecked(True)
        filter_layout.addWidget(self.check_warning)
        
        self.check_error = QCheckBox("ERROR")
        self.check_error.setChecked(True)
        filter_layout.addWidget(self.check_error)
        
        right_layout.addLayout(filter_layout)
        
        # 日志文本
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
        right_layout.addWidget(self.log_text)
        
        # 状态栏
        status_layout = QHBoxLayout()
        
        self.label_count = QLabel("日志条数: 0")
        status_layout.addWidget(self.label_count)
        
        status_layout.addStretch()
        
        self.label_file = QLabel("日志文件: ./logs/demo.log")
        status_layout.addWidget(self.label_file)
        
        right_layout.addLayout(status_layout)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # 自动日志定时器
        self.auto_log_timer = QTimer()
        self.auto_log_timer.timeout.connect(self.generate_random_log)
        
        # 统计定时器
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)
        
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
            QLineEdit, QSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QCheckBox { padding: 3px; }
        """)
    
    def send_log(self, level: str):
        """发送日志"""
        message = self.line_message.text() or f"测试{level}日志消息"
        
        log_func = getattr(self.logger, level.lower())
        log_func(message)
        
        self.line_message.clear()
    
    def toggle_auto_log(self, state: int):
        """切换自动日志"""
        if state == Qt.CheckState.Checked.value:
            interval = self.spin_interval.value()
            self.auto_log_timer.start(interval)
            self.logger.info(f"开始自动日志，间隔 {interval}ms")
        else:
            self.auto_log_timer.stop()
            self.logger.info("停止自动日志")
    
    def generate_random_log(self):
        """生成随机日志"""
        import random
        
        messages = [
            ("DEBUG", "调试信息: 变量值 x=123"),
            ("INFO", "数据采集完成，共 1000 个数据点"),
            ("INFO", "温度读数: 298.5 K"),
            ("WARNING", "温度接近上限警告"),
            ("INFO", "电压设置: 1.5 V"),
            ("DEBUG", "串口接收到 64 字节"),
            ("WARNING", "通信超时，正在重试..."),
            ("INFO", "配置已保存"),
        ]
        
        level, message = random.choice(messages)
        log_func = getattr(self.logger, level.lower())
        log_func(message)
    
    def simulate_error(self):
        """模拟异常"""
        try:
            self.logger.info("开始执行可能出错的操作...")
            result = 1 / 0
        except Exception as e:
            self.logger.error(f"发生异常: {e}", exc_info=True)
    
    def change_level(self, level: str):
        """改变日志级别"""
        logging.getLogger().setLevel(getattr(logging, level))
        self.logger.info(f"日志级别已更改为: {level}")
    
    def apply_filter(self, text: str):
        """应用过滤"""
        # 简单的文本高亮过滤
        # 实际应用中可以实现更复杂的过滤逻辑
        pass
    
    def update_stats(self):
        """更新统计"""
        # 统计日志行数
        text = self.log_text.toPlainText()
        lines = text.count('\n') + 1 if text else 0
        self.label_count.setText(f"日志条数: {lines}")
        
        # 限制最大行数
        max_lines = self.spin_max_lines.value()
        if lines > max_lines:
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.movePosition(cursor.MoveOperation.Down, 
                              cursor.MoveMode.KeepAnchor, 
                              lines - max_lines)
            cursor.removeSelectedText()
    
    def open_log_file(self):
        """打开日志文件"""
        log_file = "./logs/demo.log"
        if os.path.exists(log_file):
            os.startfile(log_file) if sys.platform == 'win32' else os.system(f'xdg-open "{log_file}"')
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "日志文件不存在")
    
    def open_log_folder(self):
        """打开日志目录"""
        log_dir = "./logs"
        if os.path.exists(log_dir):
            os.startfile(log_dir) if sys.platform == 'win32' else os.system(f'xdg-open "{log_dir}"')
        else:
            os.makedirs(log_dir, exist_ok=True)
            os.startfile(log_dir) if sys.platform == 'win32' else os.system(f'xdg-open "{log_dir}"')
    
    def export_log(self):
        """导出日志"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出日志", 
            f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                
                self.logger.info(f"日志已导出: {filename}")
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "成功", f"日志已导出:\n{filename}")
            except Exception as e:
                self.logger.error(f"导出失败: {e}")
    
    def closeEvent(self, event):
        """关闭窗口"""
        self.auto_log_timer.stop()
        self.stats_timer.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = LogViewerDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

