# Qt Designer 使用示例

本目录包含使用Qt Designer设计的界面示例。

## 文件说明

| 文件 | 说明 |
|------|------|
| `experiment_ui.ui` | Qt Designer设计的UI文件 |
| `ui_experiment.py` | 由.ui文件转换的Python代码 |
| `main.py` | 使用UI文件的主程序 |

## 使用方法

### 方法一：直接加载.ui文件

```python
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("experiment_ui.ui", self)
```

### 方法二：转换为Python代码

```bash
# 将.ui文件转换为.py
pyuic6 -x experiment_ui.ui -o ui_experiment.py

# 然后在代码中导入使用
from ui_experiment import Ui_Form
```

## 安装Qt Designer

```bash
pip install pyqt6-tools
```

启动命令:
- Windows: `pyqt6-tools designer`
- 或在Python环境的Scripts目录下找到 `designer.exe`

