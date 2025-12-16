"""
示例程序：文件对话框与数据导入
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示PyQt文件对话框的使用：
    - 打开单个/多个文件
    - 保存文件
    - 选择目录
    - CSV/TXT数据导入导出

运行方式：
    python file_dialog.py
"""

import sys
import os
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QFormLayout,
    QFileDialog, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt


class FileDialogDemo(QMainWindow):
    """文件对话框演示"""
    
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("文件对话框与数据导入")
        self.setMinimumSize(800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：按钮面板
        left_panel = QWidget()
        left_panel.setFixedWidth(280)
        left_layout = QVBoxLayout(left_panel)
        
        # 打开文件组
        open_group = QGroupBox("打开文件")
        open_layout = QVBoxLayout()
        
        btn_open_single = QPushButton("📄 打开单个文件")
        btn_open_single.clicked.connect(self.open_single_file)
        open_layout.addWidget(btn_open_single)
        
        btn_open_multi = QPushButton("📑 打开多个文件")
        btn_open_multi.clicked.connect(self.open_multiple_files)
        open_layout.addWidget(btn_open_multi)
        
        btn_open_csv = QPushButton("📊 导入CSV数据")
        btn_open_csv.clicked.connect(self.import_csv)
        open_layout.addWidget(btn_open_csv)
        
        open_group.setLayout(open_layout)
        left_layout.addWidget(open_group)
        
        # 保存文件组
        save_group = QGroupBox("保存文件")
        save_layout = QVBoxLayout()
        
        btn_save = QPushButton("💾 保存文件")
        btn_save.clicked.connect(self.save_file)
        save_layout.addWidget(btn_save)
        
        btn_export_csv = QPushButton("📤 导出为CSV")
        btn_export_csv.clicked.connect(self.export_csv)
        save_layout.addWidget(btn_export_csv)
        
        save_group.setLayout(save_layout)
        left_layout.addWidget(save_group)
        
        # 目录选择组
        dir_group = QGroupBox("目录操作")
        dir_layout = QVBoxLayout()
        
        btn_select_dir = QPushButton("📁 选择目录")
        btn_select_dir.clicked.connect(self.select_directory)
        dir_layout.addWidget(btn_select_dir)
        
        dir_group.setLayout(dir_layout)
        left_layout.addWidget(dir_group)
        
        # 生成测试数据
        test_group = QGroupBox("测试数据")
        test_layout = QVBoxLayout()
        
        btn_generate = QPushButton("🔢 生成测试数据")
        btn_generate.clicked.connect(self.generate_test_data)
        test_layout.addWidget(btn_generate)
        
        test_group.setLayout(test_layout)
        left_layout.addWidget(test_group)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)
        
        # 右侧：显示区域
        right_layout = QVBoxLayout()
        
        # 文件列表
        file_group = QGroupBox("选择的文件")
        file_layout = QVBoxLayout()
        self.list_files = QListWidget()
        file_layout.addWidget(self.list_files)
        file_group.setLayout(file_layout)
        right_layout.addWidget(file_group)
        
        # 数据预览
        data_group = QGroupBox("数据预览")
        data_layout = QVBoxLayout()
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        data_layout.addWidget(self.text_preview)
        data_group.setLayout(data_layout)
        right_layout.addWidget(data_group)
        
        # 状态标签
        self.label_status = QLabel("就绪")
        self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")
        right_layout.addWidget(self.label_status)
        
        main_layout.addLayout(right_layout)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
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
            }
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
    
    def open_single_file(self):
        """打开单个文件"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "打开文件",
            "",
            "所有文件 (*);;文本文件 (*.txt);;数据文件 (*.csv *.dat)"
        )
        
        if filename:
            self.list_files.clear()
            self.list_files.addItem(filename)
            self.preview_file(filename)
            self.set_status(f"已打开: {os.path.basename(filename)}")
    
    def open_multiple_files(self):
        """打开多个文件"""
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "选择多个文件",
            "",
            "数据文件 (*.csv *.txt *.dat);;所有文件 (*)"
        )
        
        if filenames:
            self.list_files.clear()
            for filename in filenames:
                self.list_files.addItem(filename)
            
            self.text_preview.setText(f"选择了 {len(filenames)} 个文件:\n")
            for f in filenames:
                self.text_preview.append(f"  • {os.path.basename(f)}")
            
            self.set_status(f"选择了 {len(filenames)} 个文件")
    
    def import_csv(self):
        """导入CSV数据"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "导入CSV数据",
            "",
            "CSV文件 (*.csv);;文本文件 (*.txt);;所有文件 (*)"
        )
        
        if filename:
            try:
                # 尝试加载数据
                self.current_data = np.loadtxt(filename, delimiter=',', skiprows=1)
                
                rows, cols = self.current_data.shape
                
                # 显示预览
                preview = f"文件: {os.path.basename(filename)}\n"
                preview += f"形状: {rows} 行 × {cols} 列\n"
                preview += "-" * 40 + "\n"
                preview += "数据预览 (前10行):\n"
                
                for i in range(min(10, rows)):
                    row_str = "  ".join(f"{v:10.4g}" for v in self.current_data[i])
                    preview += f"{i+1:3d}: {row_str}\n"
                
                if rows > 10:
                    preview += f"  ... 还有 {rows - 10} 行\n"
                
                preview += "-" * 40 + "\n"
                preview += f"统计信息:\n"
                for j in range(cols):
                    col_data = self.current_data[:, j]
                    preview += f"  列{j+1}: 最小={col_data.min():.4g}, "
                    preview += f"最大={col_data.max():.4g}, "
                    preview += f"平均={col_data.mean():.4g}\n"
                
                self.text_preview.setText(preview)
                self.list_files.clear()
                self.list_files.addItem(filename)
                self.set_status(f"成功导入 {rows}×{cols} 数据矩阵")
                
            except Exception as e:
                QMessageBox.critical(self, "导入错误", f"无法导入文件:\n{str(e)}")
                self.set_status("导入失败", error=True)
    
    def save_file(self):
        """保存文件"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            "output.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if filename:
            try:
                content = self.text_preview.toPlainText()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.set_status(f"已保存: {os.path.basename(filename)}")
                QMessageBox.information(self, "保存成功", f"文件已保存:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "保存错误", f"保存失败:\n{str(e)}")
    
    def export_csv(self):
        """导出为CSV"""
        if self.current_data is None:
            QMessageBox.warning(self, "警告", "没有数据可导出。\n请先导入数据或生成测试数据。")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出CSV",
            "data.csv",
            "CSV文件 (*.csv)"
        )
        
        if filename:
            try:
                # 生成表头
                cols = self.current_data.shape[1]
                header = ",".join(f"Col{i+1}" for i in range(cols))
                
                np.savetxt(filename, self.current_data, delimiter=',', 
                          header=header, comments='')
                
                self.set_status(f"已导出: {os.path.basename(filename)}")
                QMessageBox.information(self, "导出成功", f"数据已导出:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出失败:\n{str(e)}")
    
    def select_directory(self):
        """选择目录"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择目录",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            # 列出目录中的文件
            files = os.listdir(folder)
            data_files = [f for f in files if f.endswith(('.csv', '.txt', '.dat'))]
            
            self.list_files.clear()
            for f in data_files:
                self.list_files.addItem(os.path.join(folder, f))
            
            self.text_preview.setText(f"目录: {folder}\n")
            self.text_preview.append(f"数据文件数量: {len(data_files)}\n")
            self.text_preview.append("-" * 40)
            
            for f in data_files[:20]:
                size = os.path.getsize(os.path.join(folder, f)) / 1024
                self.text_preview.append(f"  {f} ({size:.1f} KB)")
            
            if len(data_files) > 20:
                self.text_preview.append(f"  ... 还有 {len(data_files) - 20} 个文件")
            
            self.set_status(f"找到 {len(data_files)} 个数据文件")
    
    def generate_test_data(self):
        """生成测试数据"""
        # 生成模拟光谱数据
        x = np.linspace(400, 700, 301)  # 波长 400-700 nm
        
        # 多个高斯峰
        y = (0.8 * np.exp(-((x - 450)**2) / (2 * 15**2)) +
             1.0 * np.exp(-((x - 520)**2) / (2 * 20**2)) +
             0.6 * np.exp(-((x - 600)**2) / (2 * 25**2)))
        
        # 添加噪声
        y += np.random.randn(len(x)) * 0.05
        
        # 存储数据
        self.current_data = np.column_stack([x, y])
        
        # 显示预览
        preview = "生成的测试数据（模拟光谱）:\n"
        preview += f"形状: {len(x)} 行 × 2 列\n"
        preview += "列: 波长(nm), 强度(a.u.)\n"
        preview += "-" * 40 + "\n"
        
        for i in range(min(15, len(x))):
            preview += f"{x[i]:6.1f} nm,  {y[i]:8.4f}\n"
        
        preview += "  ...\n"
        preview += "-" * 40 + "\n"
        preview += f"波长范围: {x.min():.1f} - {x.max():.1f} nm\n"
        preview += f"强度范围: {y.min():.4f} - {y.max():.4f}\n"
        
        self.text_preview.setText(preview)
        self.set_status("已生成测试数据 (301×2)")
    
    def preview_file(self, filename: str):
        """预览文件内容"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read(5000)  # 只读取前5000字符
            
            if len(content) == 5000:
                content += "\n... (文件过大，只显示前5000字符)"
            
            self.text_preview.setText(content)
            
        except Exception as e:
            self.text_preview.setText(f"无法预览文件:\n{str(e)}")
    
    def set_status(self, message: str, error: bool = False):
        """设置状态"""
        self.label_status.setText(message)
        if error:
            self.label_status.setStyleSheet("color: #e74c3c; padding: 5px;")
        else:
            self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")


def main():
    app = QApplication(sys.argv)
    window = FileDialogDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

