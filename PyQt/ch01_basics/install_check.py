"""
示例程序：环境检测脚本
所属章节：第一章 - PyQt基础入门

功能说明：
    检查PyQt6及相关科学计算包是否正确安装
    
运行方式：
    python install_check.py
"""

import sys


def check_package(name: str) -> tuple[bool, str]:
    """
    检查包是否可导入
    
    Args:
        name: 包的导入名称
        
    Returns:
        (是否成功, 版本信息或错误信息)
    """
    try:
        module = __import__(name)
        version = getattr(module, '__version__', '未知版本')
        # 特殊处理PyQt6
        if name == 'PyQt6':
            from PyQt6.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
            version = f"PyQt {PYQT_VERSION_STR} / Qt {QT_VERSION_STR}"
        return True, version
    except ImportError as e:
        return False, str(e)


def main():
    """主函数：执行环境检查"""
    
    # 需要检查的包列表
    packages = {
        "PyQt6": "PyQt6",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "SciPy": "scipy",
        "PySerial": "serial"
    }
    
    print()
    print("=" * 60)
    print("     PyQt科研应用编程教程 - 环境检查")
    print("=" * 60)
    print()
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    print()
    print("-" * 60)
    print(f"{'包名':<15} {'状态':<10} {'版本信息'}")
    print("-" * 60)
    
    all_ok = True
    results = []
    
    for display_name, import_name in packages.items():
        success, info = check_package(import_name)
        status = "✓ 已安装" if success else "✗ 未安装"
        if not success:
            all_ok = False
        results.append((display_name, status, info if success else ""))
        print(f"{display_name:<15} {status:<10} {info if success else ''}")
    
    print("-" * 60)
    print()
    
    if all_ok:
        print("✓ 环境配置完成，所有依赖包均已安装！")
        print()
        print("你可以开始学习PyQt编程了。运行以下命令测试第一个窗口：")
        print("    python first_window.py")
    else:
        print("✗ 部分依赖包未安装。请运行以下命令安装：")
        print("    pip install -r requirements.txt")
        print()
        print("或者单独安装缺失的包：")
        print("    pip install PyQt6 numpy matplotlib scipy pyserial")
    
    print()
    print("=" * 60)
    
    # 如果PyQt6已安装，展示一个简单的GUI测试
    if check_package("PyQt6")[0]:
        print()
        response = input("是否运行GUI测试窗口？(y/n): ").strip().lower()
        if response == 'y':
            run_gui_test()


def run_gui_test():
    """运行一个简单的GUI测试窗口"""
    from PyQt6.QtWidgets import QApplication, QMessageBox
    
    app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("环境测试")
    msg.setText("PyQt6 环境测试成功！")
    msg.setInformativeText("你的开发环境已经准备就绪，可以开始学习PyQt编程了。")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


if __name__ == "__main__":
    main()

