# 应用打包指南

## 环境准备

### 1. 安装PyInstaller

```bash
pip install pyinstaller
```

### 2. 安装UPX（可选，用于压缩）

- Windows: 从 https://github.com/upx/upx/releases 下载
- Linux: `sudo apt install upx`
- macOS: `brew install upx`

## 打包方法

### 方法一：使用构建脚本

```bash
# 打包为目录
python build.py

# 打包为单文件
python build.py --onefile

# 仅生成spec文件
python build.py --spec-only

# 清理构建文件
python build.py --clean
```

### 方法二：直接使用PyInstaller

```bash
# 基本打包
pyinstaller --windowed main.py

# 单文件打包
pyinstaller --onefile --windowed main.py

# 使用spec文件
pyinstaller InstrumentControl.spec
```

## spec文件配置

### 添加数据文件

```python
datas=[
    ('resources', 'resources'),  # (源路径, 目标路径)
    ('config/*.yaml', 'config'),
]
```

### 添加隐藏导入

```python
hiddenimports=[
    'PyQt6.QtPrintSupport',
    'numpy',
    'scipy.signal',
]
```

### 排除不需要的模块

```python
excludes=[
    'tkinter',
    'unittest',
    'email',
]
```

## 常见问题

### 1. 找不到模块

添加到 `hiddenimports` 列表中。

### 2. 资源文件缺失

使用正确的路径访问资源：

```python
import sys
import os

def resource_path(relative_path):
    """获取资源文件路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller打包后的路径
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
```

### 3. 文件太大

- 使用 `--exclude-module` 排除不需要的模块
- 使用UPX压缩
- 考虑使用虚拟环境减少依赖

### 4. 杀毒软件误报

- 使用代码签名
- 将程序添加到白名单
- 联系杀软厂商申请误报

## 跨平台打包

### Windows

```bash
pyinstaller --onefile --windowed --icon=app.ico main.py
```

### macOS

```bash
pyinstaller --onefile --windowed --icon=app.icns main.py
```

### Linux

```bash
pyinstaller --onefile main.py
```

## 创建安装程序

### Windows (Inno Setup)

1. 下载安装 Inno Setup
2. 使用向导创建安装脚本
3. 编译生成安装程序

### macOS

```bash
# 创建DMG
hdiutil create -volname "InstrumentControl" -srcfolder dist/InstrumentControl -ov -format UDZO InstrumentControl.dmg
```

### Linux

```bash
# 创建AppImage
# 参考 https://appimage.org/
```

## 版本信息

在Windows上添加版本信息，创建 `version_info.txt`：

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'Physics Lab'),
        StringStruct('ProductName', 'Instrument Control'),
        StringStruct('ProductVersion', '1.0.0'),
      ])
    ])
  ]
)
```

然后在spec文件中使用：

```python
exe = EXE(
    ...
    version='version_info.txt',
)
```

