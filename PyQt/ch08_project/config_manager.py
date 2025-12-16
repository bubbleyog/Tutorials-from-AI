"""
示例程序：配置文件管理
所属章节：第八章 - 项目实战与部署

功能说明：
    演示配置管理系统：
    - YAML/JSON配置读写
    - 单例模式
    - 默认值处理
    - GUI配置编辑器

运行方式：
    python config_manager.py
"""

import sys
import os
import json
from pathlib import Path
from typing import Any, Optional, Dict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QGroupBox, QFormLayout,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget,
    QTextEdit, QFileDialog, QMessageBox, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt

# 尝试导入yaml
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ============================================================
# 配置管理器
# ============================================================

class ConfigManager:
    """
    配置管理器（单例模式）
    
    支持YAML和JSON格式的配置文件
    """
    
    _instance = None
    
    # 默认配置
    DEFAULT_CONFIG = {
        'app': {
            'name': 'Instrument Control',
            'version': '1.0.0',
            'theme': 'dark',
            'language': 'zh_CN'
        },
        'window': {
            'width': 1200,
            'height': 800,
            'remember_position': True,
            'start_maximized': False
        },
        'instruments': {
            'temperature_controller': {
                'enabled': True,
                'port': 'COM3',
                'baudrate': 9600,
                'timeout': 1.0
            },
            'power_supply': {
                'enabled': True,
                'host': '192.168.1.100',
                'port': 5025
            }
        },
        'data': {
            'auto_save': True,
            'save_interval': 60,
            'save_path': './data',
            'format': 'csv'
        },
        'logging': {
            'level': 'INFO',
            'file': './logs/app.log',
            'max_size': 10485760,
            'backup_count': 5
        },
        'plot': {
            'refresh_rate': 10,
            'history_length': 1000,
            'grid': True,
            'legend': True
        }
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = cls.DEFAULT_CONFIG.copy()
            cls._instance._config_path = None
        return cls._instance
    
    def load(self, config_path: str) -> bool:
        """加载配置文件"""
        path = Path(config_path)
        
        if not path.exists():
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    if YAML_AVAILABLE:
                        loaded = yaml.safe_load(f)
                    else:
                        raise ImportError("YAML support requires pyyaml")
                else:
                    loaded = json.load(f)
            
            # 合并配置（保留默认值）
            self._merge_config(self._config, loaded)
            self._config_path = config_path
            return True
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            return False
    
    def _merge_config(self, base: dict, update: dict):
        """递归合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def save(self, config_path: str = None) -> bool:
        """保存配置"""
        path = Path(config_path or self._config_path)
        
        if not path:
            return False
        
        try:
            # 创建目录
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    if YAML_AVAILABLE:
                        yaml.dump(self._config, f, allow_unicode=True, 
                                 default_flow_style=False)
                    else:
                        raise ImportError("YAML support requires pyyaml")
                else:
                    json.dump(self._config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        支持点号分隔的路径，如 'app.name'
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取配置节"""
        return self._config.get(section, {})
    
    def reset(self):
        """重置为默认配置"""
        self._config = self.DEFAULT_CONFIG.copy()
    
    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self._config


# ============================================================
# 配置编辑器GUI
# ============================================================

class ConfigEditorWidget(QWidget):
    """配置节编辑器"""
    
    def __init__(self, section_name: str, section_config: dict):
        super().__init__()
        self.section_name = section_name
        self.section_config = section_config
        self.widgets = {}
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        for key, value in self.section_config.items():
            widget = self.create_widget(key, value)
            if widget:
                self.widgets[key] = widget
                layout.addRow(key + ":", widget)
    
    def create_widget(self, key: str, value: Any) -> Optional[QWidget]:
        """根据值类型创建控件"""
        if isinstance(value, bool):
            widget = QCheckBox()
            widget.setChecked(value)
            return widget
            
        elif isinstance(value, int):
            widget = QSpinBox()
            widget.setRange(-1000000, 1000000)
            widget.setValue(value)
            return widget
            
        elif isinstance(value, float):
            widget = QDoubleSpinBox()
            widget.setRange(-1000000, 1000000)
            widget.setDecimals(3)
            widget.setValue(value)
            return widget
            
        elif isinstance(value, str):
            widget = QLineEdit()
            widget.setText(value)
            return widget
            
        elif isinstance(value, dict):
            # 嵌套字典显示为只读文本
            widget = QLineEdit()
            widget.setText(str(value))
            widget.setReadOnly(True)
            widget.setStyleSheet("background-color: #f0f0f0;")
            return widget
        
        return None
    
    def get_values(self) -> dict:
        """获取当前值"""
        result = {}
        
        for key, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                result[key] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                result[key] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                result[key] = widget.value()
            elif isinstance(widget, QLineEdit):
                result[key] = widget.text()
        
        return result


class ConfigManagerDemo(QMainWindow):
    """配置管理器演示"""
    
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.section_editors = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("配置管理器")
        self.setMinimumSize(900, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：配置树
        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        
        # 文件操作
        file_group = QGroupBox("配置文件")
        file_layout = QVBoxLayout()
        
        btn_load = QPushButton("📂 加载配置")
        btn_load.clicked.connect(self.load_config)
        file_layout.addWidget(btn_load)
        
        btn_save = QPushButton("💾 保存配置")
        btn_save.clicked.connect(self.save_config)
        file_layout.addWidget(btn_save)
        
        btn_export = QPushButton("📤 导出为JSON")
        btn_export.clicked.connect(self.export_json)
        file_layout.addWidget(btn_export)
        
        if YAML_AVAILABLE:
            btn_export_yaml = QPushButton("📤 导出为YAML")
            btn_export_yaml.clicked.connect(self.export_yaml)
            file_layout.addWidget(btn_export_yaml)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # 配置树
        tree_group = QGroupBox("配置结构")
        tree_layout = QVBoxLayout()
        
        self.config_tree = QTreeWidget()
        self.config_tree.setHeaderLabels(["配置节"])
        self.config_tree.itemClicked.connect(self.on_tree_item_clicked)
        tree_layout.addWidget(self.config_tree)
        
        tree_group.setLayout(tree_layout)
        left_layout.addWidget(tree_group)
        
        # 操作按钮
        btn_reset = QPushButton("🔄 重置为默认")
        btn_reset.clicked.connect(self.reset_config)
        left_layout.addWidget(btn_reset)
        
        main_layout.addWidget(left_panel)
        
        # 右侧：配置编辑
        right_layout = QVBoxLayout()
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 为每个配置节创建标签页
        for section_name, section_config in self.config.config.items():
            if isinstance(section_config, dict):
                editor = ConfigEditorWidget(section_name, section_config)
                self.section_editors[section_name] = editor
                self.tabs.addTab(editor, section_name.capitalize())
        
        right_layout.addWidget(self.tabs)
        
        # 预览
        preview_group = QGroupBox("配置预览 (JSON)")
        preview_layout = QVBoxLayout()
        
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setMaximumHeight(200)
        self.text_preview.setStyleSheet("""
            font-family: Consolas, monospace;
            font-size: 11px;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        preview_layout.addWidget(self.text_preview)
        
        btn_refresh_preview = QPushButton("刷新预览")
        btn_refresh_preview.clicked.connect(self.refresh_preview)
        preview_layout.addWidget(btn_refresh_preview)
        
        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)
        
        main_layout.addLayout(right_layout)
        
        # 初始化
        self.refresh_tree()
        self.refresh_preview()
        
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
            QLineEdit, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 2px solid #3498db;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 15px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTreeWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def refresh_tree(self):
        """刷新配置树"""
        self.config_tree.clear()
        
        for section_name, section_config in self.config.config.items():
            section_item = QTreeWidgetItem([section_name])
            self.config_tree.addTopLevelItem(section_item)
            
            if isinstance(section_config, dict):
                for key in section_config.keys():
                    key_item = QTreeWidgetItem([key])
                    section_item.addChild(key_item)
        
        self.config_tree.expandAll()
    
    def refresh_preview(self):
        """刷新预览"""
        # 先应用编辑器中的更改
        for section_name, editor in self.section_editors.items():
            values = editor.get_values()
            for key, value in values.items():
                self.config.set(f"{section_name}.{key}", value)
        
        # 显示JSON
        preview = json.dumps(self.config.config, ensure_ascii=False, indent=2)
        self.text_preview.setText(preview)
    
    def on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """点击配置树项"""
        # 如果是顶级项（配置节），切换到对应标签页
        if item.parent() is None:
            section_name = item.text(0)
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i).lower() == section_name:
                    self.tabs.setCurrentIndex(i)
                    break
    
    def load_config(self):
        """加载配置文件"""
        filter_str = "配置文件 (*.json *.yaml *.yml);;JSON (*.json)"
        if YAML_AVAILABLE:
            filter_str = "配置文件 (*.json *.yaml *.yml);;YAML (*.yaml *.yml);;JSON (*.json)"
        
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载配置", "", filter_str
        )
        
        if filename:
            if self.config.load(filename):
                # 重新创建编辑器
                self.tabs.clear()
                self.section_editors.clear()
                
                for section_name, section_config in self.config.config.items():
                    if isinstance(section_config, dict):
                        editor = ConfigEditorWidget(section_name, section_config)
                        self.section_editors[section_name] = editor
                        self.tabs.addTab(editor, section_name.capitalize())
                
                self.refresh_tree()
                self.refresh_preview()
                QMessageBox.information(self, "成功", f"配置已加载:\n{filename}")
            else:
                QMessageBox.critical(self, "错误", "加载配置失败")
    
    def save_config(self):
        """保存配置"""
        self.refresh_preview()  # 先应用更改
        
        filter_str = "JSON (*.json)"
        if YAML_AVAILABLE:
            filter_str = "YAML (*.yaml);;JSON (*.json)"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存配置", "config.yaml" if YAML_AVAILABLE else "config.json",
            filter_str
        )
        
        if filename:
            if self.config.save(filename):
                QMessageBox.information(self, "成功", f"配置已保存:\n{filename}")
            else:
                QMessageBox.critical(self, "错误", "保存配置失败")
    
    def export_json(self):
        """导出为JSON"""
        self.refresh_preview()
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出JSON", "config.json", "JSON (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.config.config, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", f"已导出:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))
    
    def export_yaml(self):
        """导出为YAML"""
        if not YAML_AVAILABLE:
            return
        
        self.refresh_preview()
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出YAML", "config.yaml", "YAML (*.yaml)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    yaml.dump(self.config.config, f, allow_unicode=True,
                             default_flow_style=False)
                QMessageBox.information(self, "成功", f"已导出:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))
    
    def reset_config(self):
        """重置配置"""
        reply = QMessageBox.question(
            self, "确认", "确定要重置为默认配置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config.reset()
            
            # 重新创建编辑器
            self.tabs.clear()
            self.section_editors.clear()
            
            for section_name, section_config in self.config.config.items():
                if isinstance(section_config, dict):
                    editor = ConfigEditorWidget(section_name, section_config)
                    self.section_editors[section_name] = editor
                    self.tabs.addTab(editor, section_name.capitalize())
            
            self.refresh_tree()
            self.refresh_preview()


def main():
    app = QApplication(sys.argv)
    window = ConfigManagerDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

