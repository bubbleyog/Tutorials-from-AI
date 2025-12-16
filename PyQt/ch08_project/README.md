# 第八章：项目实战与部署

> 本章将学习如何组织完整的PyQt项目，并打包部署

## 本章内容

- [8.1 项目结构组织](#81-项目结构组织)
- [8.2 配置文件管理](#82-配置文件管理)
- [8.3 日志系统](#83-日志系统)
- [8.4 应用打包](#84-应用打包)
- [8.5 完整项目示例](#85-完整项目示例)

---

## 8.1 项目结构组织

### 推荐项目结构

```
my_instrument_app/
├── src/                        # 源代码
│   ├── __init__.py
│   ├── main.py                 # 入口文件
│   ├── app.py                  # 应用程序类
│   ├── ui/                     # 界面模块
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── dialogs/
│   │   └── widgets/
│   ├── core/                   # 核心逻辑
│   │   ├── __init__.py
│   │   ├── instrument.py
│   │   ├── data_processor.py
│   │   └── config.py
│   ├── communication/          # 通信模块
│   │   ├── __init__.py
│   │   ├── serial_comm.py
│   │   └── tcp_comm.py
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       └── helpers.py
├── resources/                  # 资源文件
│   ├── icons/
│   ├── images/
│   └── styles/
├── config/                     # 配置文件
│   ├── default.yaml
│   └── instruments.yaml
├── tests/                      # 测试
│   ├── __init__.py
│   ├── test_instrument.py
│   └── test_data_processor.py
├── docs/                       # 文档
│   └── user_manual.md
├── scripts/                    # 构建脚本
│   ├── build.py
│   └── build.spec
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

### 模块职责划分

| 模块 | 职责 |
|------|------|
| `ui/` | 界面展示、用户交互 |
| `core/` | 业务逻辑、数据处理 |
| `communication/` | 仪器通信、协议解析 |
| `utils/` | 通用工具函数 |

### 入口文件示例

```python
# src/main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.app import InstrumentApp

def main():
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("Instrument Control")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Physics Lab")
    
    # 创建主应用
    main_app = InstrumentApp()
    main_app.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## 8.2 配置文件管理

**示例程序**：[config_manager.py](config_manager.py)

### 配置文件格式选择

| 格式 | 优点 | 缺点 |
|------|------|------|
| YAML | 可读性强、支持注释 | 需要额外库 |
| JSON | 原生支持、通用 | 不支持注释 |
| INI | 简单、原生支持 | 结构简单 |
| TOML | 现代、可读性强 | 较新 |

### YAML配置示例

```yaml
# config/default.yaml
app:
  name: "Instrument Control"
  version: "1.0.0"
  theme: "dark"
  language: "zh_CN"

window:
  width: 1200
  height: 800
  remember_position: true

instruments:
  temperature_controller:
    port: "COM3"
    baudrate: 9600
    timeout: 1.0
    
  power_supply:
    host: "192.168.1.100"
    port: 5025

data:
  auto_save: true
  save_interval: 60
  save_path: "./data"
  
logging:
  level: "INFO"
  file: "./logs/app.log"
  max_size: 10485760  # 10MB
  backup_count: 5
```

### 配置管理类

```python
import yaml
from pathlib import Path

class ConfigManager:
    """配置管理器"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
        return cls._instance
    
    def load(self, config_path: str):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """获取配置值，支持点号分隔的路径"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value):
        """设置配置值"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def save(self, config_path: str):
        """保存配置"""
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, allow_unicode=True)
```

---

## 8.3 日志系统

**示例程序**：[logging_system.py](logging_system.py)

### Python logging模块

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str, level: str = "INFO"):
    """配置日志系统"""
    
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
```

### 在PyQt中使用

```python
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
    def connect_instrument(self):
        try:
            self.logger.info("正在连接仪器...")
            # 连接逻辑
            self.logger.info("连接成功")
        except Exception as e:
            self.logger.error(f"连接失败: {e}", exc_info=True)
```

### 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 调试信息 |
| INFO | 常规信息 |
| WARNING | 警告信息 |
| ERROR | 错误信息 |
| CRITICAL | 严重错误 |

---

## 8.4 应用打包

**相关文件**：[build_scripts/](build_scripts/)

### PyInstaller打包

#### 安装

```bash
pip install pyinstaller
```

#### 基本命令

```bash
# 单文件打包
pyinstaller --onefile --windowed src/main.py

# 使用spec文件
pyinstaller build.spec
```

#### spec文件示例

```python
# build.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('config', 'config'),
    ],
    hiddenimports=[
        'PyQt6.QtPrintSupport',
        'numpy',
        'scipy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InstrumentControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/app.ico',
)
```

### 常见问题

1. **找不到模块**：添加到 `hiddenimports`
2. **资源文件缺失**：添加到 `datas`
3. **文件太大**：使用 `--exclude-module` 排除不需要的模块

### 跨平台打包

```bash
# Windows
pyinstaller --onefile --windowed --icon=app.ico main.py

# macOS
pyinstaller --onefile --windowed --icon=app.icns main.py

# Linux
pyinstaller --onefile main.py
```

---

## 8.5 完整项目示例

**示例程序**：[complete_project/](complete_project/)

### 项目功能

一个完整的**低温测量系统控制软件**，包含：

1. **仪器管理**
   - 温度控制器连接
   - 电源控制
   - 万用表读数

2. **数据采集**
   - 多通道同步采集
   - 实时曲线显示
   - 数据自动保存

3. **用户界面**
   - 深色主题
   - 停靠面板
   - 状态栏

4. **系统功能**
   - 配置管理
   - 日志记录
   - 错误处理

---

## 本章小结

通过本章学习，你应该掌握了：

1. **项目结构**：模块化组织、职责分离
2. **配置管理**：YAML配置、单例模式
3. **日志系统**：logging模块、文件轮转
4. **应用打包**：PyInstaller、spec文件
5. **完整项目**：整合所有知识

### 开发检查清单

```
□ 项目结构合理
□ 配置文件管理
□ 日志系统完善
□ 错误处理完整
□ 代码注释充分
□ 单元测试覆盖
□ 用户文档完整
□ 打包测试通过
```

### 性能优化建议

1. **图形更新**：使用定时器控制刷新率
2. **数据处理**：大数据使用NumPy
3. **通信优化**：批量读写、异步处理
4. **内存管理**：及时释放大对象

---

## 教程总结

恭喜你完成了全部8章的学习！

### 回顾

| 章节 | 内容 |
|------|------|
| 第一章 | PyQt基础、窗口、控件 |
| 第二章 | 布局管理、界面设计 |
| 第三章 | 信号与槽机制 |
| 第四章 | Matplotlib科研绑图 |
| 第五章 | 数据处理与分析 |
| 第六章 | 仪器通信基础 |
| 第七章 | 仪器控制界面实战 |
| 第八章 | 项目实战与部署 |

### 下一步

1. 动手实践：选择一个实际项目开始开发
2. 深入学习：Qt Designer、QML
3. 扩展知识：数据库、Web服务
4. 社区交流：分享经验、获取帮助

祝你在物理研究中充分利用PyQt！🎉

