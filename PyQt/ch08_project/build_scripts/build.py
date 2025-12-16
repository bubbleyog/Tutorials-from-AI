"""
构建脚本
所属章节：第八章 - 项目实战与部署

功能说明：
    自动化构建PyQt应用程序：
    - 生成PyInstaller spec文件
    - 执行打包命令
    - 清理临时文件

使用方法：
    python build.py [--onefile] [--clean]
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path


# ============================================================
# 构建配置
# ============================================================

CONFIG = {
    'name': 'InstrumentControl',
    'version': '1.0.0',
    'author': 'Physics Lab',
    'description': '仪器控制软件',
    
    # 入口文件
    'entry_point': 'main.py',
    
    # 包含的数据文件 (源路径, 目标路径)
    'datas': [
        ('resources', 'resources'),
        ('config', 'config'),
    ],
    
    # 隐藏导入
    'hidden_imports': [
        'PyQt6.QtPrintSupport',
        'numpy',
        'scipy',
        'matplotlib',
    ],
    
    # 排除模块
    'excludes': [
        'tkinter',
        'unittest',
    ],
    
    # 图标文件
    'icon': 'resources/icons/app.ico',
    
    # 是否显示控制台
    'console': False,
}


# ============================================================
# 构建函数
# ============================================================

def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} 已安装")
        return True
    except ImportError:
        print("✗ PyInstaller 未安装")
        print("  运行: pip install pyinstaller")
        return False


def generate_spec_file(onefile: bool = False) -> str:
    """生成spec文件"""
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# 自动生成的spec文件
# 应用名称: {CONFIG['name']}
# 版本: {CONFIG['version']}

block_cipher = None

# 数据文件
datas = {CONFIG['datas']}

# 隐藏导入
hiddenimports = {CONFIG['hidden_imports']}

a = Analysis(
    ['{CONFIG['entry_point']}'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes={CONFIG['excludes']},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

'''

    if onefile:
        spec_content += f'''
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{CONFIG['name']}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={CONFIG['console']},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{CONFIG['icon']}' if os.path.exists('{CONFIG['icon']}') else None,
)
'''
    else:
        spec_content += f'''
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{CONFIG['name']}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console={CONFIG['console']},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{CONFIG['icon']}' if os.path.exists('{CONFIG['icon']}') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{CONFIG['name']}',
)
'''

    spec_file = f"{CONFIG['name']}.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✓ 已生成 {spec_file}")
    return spec_file


def run_pyinstaller(spec_file: str):
    """运行PyInstaller"""
    print("\n开始打包...")
    
    cmd = ['pyinstaller', '--clean', '--noconfirm', spec_file]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✓ 打包完成!")
        print(f"  输出目录: dist/{CONFIG['name']}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 打包失败: {e}")
        return False


def clean_build():
    """清理构建文件"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = [f"{CONFIG['name']}.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 已删除 {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✓ 已删除 {file_name}")
    
    print("清理完成")


def create_installer():
    """创建安装程序（仅Windows）"""
    if sys.platform != 'win32':
        print("安装程序创建仅支持Windows")
        return
    
    # 这里可以集成NSIS或Inno Setup
    print("提示: 可以使用NSIS或Inno Setup创建安装程序")


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='构建PyQt应用程序')
    parser.add_argument('--onefile', action='store_true', 
                       help='打包为单个可执行文件')
    parser.add_argument('--clean', action='store_true',
                       help='清理构建文件')
    parser.add_argument('--spec-only', action='store_true',
                       help='仅生成spec文件')
    
    args = parser.parse_args()
    
    print(f"{'='*50}")
    print(f"  {CONFIG['name']} 构建脚本")
    print(f"  版本: {CONFIG['version']}")
    print(f"{'='*50}\n")
    
    if args.clean:
        clean_build()
        return
    
    if not check_pyinstaller():
        return
    
    spec_file = generate_spec_file(onefile=args.onefile)
    
    if args.spec_only:
        print("\n仅生成spec文件，跳过打包")
        return
    
    run_pyinstaller(spec_file)


if __name__ == "__main__":
    main()

