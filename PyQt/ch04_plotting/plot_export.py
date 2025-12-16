"""
示例程序：图表导出与保存
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示图表的导出和保存功能：
    - 多格式导出（PNG, PDF, SVG, EPS）
    - DPI和尺寸设置
    - 数据导出为CSV
    - 批量导出

运行方式：
    python plot_export.py
"""

import sys
import os
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
    QGroupBox, QFormLayout, QFileDialog, QLineEdit, QCheckBox,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class PlotExportDemo(QMainWindow):
    """图表导出演示"""
    
    def __init__(self):
        super().__init__()
        
        # 存储绘图数据
        self.x_data = None
        self.y_data = None
        
        self.init_ui()
        self.generate_sample_plot()
    
    def init_ui(self):
        self.setWindowTitle("图表导出与保存")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧图形
        plot_layout = QVBoxLayout()
        
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        # 状态标签
        self.label_status = QLabel("就绪")
        self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")
        plot_layout.addWidget(self.label_status)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
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
            QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QPushButton {
                padding: 10px 16px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        title = QLabel("💾 导出设置")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 图片导出设置
        image_group = QGroupBox("图片导出")
        image_form = QFormLayout()
        
        # 格式选择
        self.combo_format = QComboBox()
        self.combo_format.addItems(["PNG", "PDF", "SVG", "EPS", "JPEG"])
        image_form.addRow("格式:", self.combo_format)
        
        # DPI设置
        self.spin_dpi = QSpinBox()
        self.spin_dpi.setRange(72, 600)
        self.spin_dpi.setValue(300)
        self.spin_dpi.setSuffix(" dpi")
        image_form.addRow("分辨率:", self.spin_dpi)
        
        # 尺寸设置
        self.spin_width = QDoubleSpinBox()
        self.spin_width.setRange(1, 20)
        self.spin_width.setValue(8)
        self.spin_width.setSuffix(" in")
        image_form.addRow("宽度:", self.spin_width)
        
        self.spin_height = QDoubleSpinBox()
        self.spin_height.setRange(1, 20)
        self.spin_height.setValue(6)
        self.spin_height.setSuffix(" in")
        image_form.addRow("高度:", self.spin_height)
        
        # 选项
        self.check_transparent = QCheckBox("透明背景")
        image_form.addRow("", self.check_transparent)
        
        self.check_tight = QCheckBox("裁剪空白")
        self.check_tight.setChecked(True)
        image_form.addRow("", self.check_tight)
        
        image_group.setLayout(image_form)
        layout.addWidget(image_group)
        
        # 保存按钮
        btn_save_image = QPushButton("📷 保存图片")
        btn_save_image.setStyleSheet("background-color: #3498db;")
        btn_save_image.clicked.connect(self.save_image)
        layout.addWidget(btn_save_image)
        
        # 数据导出
        data_group = QGroupBox("数据导出")
        data_layout = QVBoxLayout()
        
        btn_save_csv = QPushButton("📊 导出为 CSV")
        btn_save_csv.setStyleSheet("background-color: #27ae60;")
        btn_save_csv.clicked.connect(self.save_csv)
        data_layout.addWidget(btn_save_csv)
        
        btn_save_numpy = QPushButton("🔢 导出为 NumPy")
        btn_save_numpy.setStyleSheet("background-color: #9b59b6;")
        btn_save_numpy.clicked.connect(self.save_numpy)
        data_layout.addWidget(btn_save_numpy)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # 批量导出
        batch_group = QGroupBox("批量导出")
        batch_layout = QVBoxLayout()
        
        self.input_prefix = QLineEdit("plot")
        batch_layout.addWidget(QLabel("文件名前缀:"))
        batch_layout.addWidget(self.input_prefix)
        
        btn_batch = QPushButton("📁 批量导出所有格式")
        btn_batch.setStyleSheet("background-color: #e67e22;")
        btn_batch.clicked.connect(self.batch_export)
        batch_layout.addWidget(btn_batch)
        
        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)
        
        layout.addStretch()
        
        # 重新生成数据
        btn_regenerate = QPushButton("🔄 重新生成数据")
        btn_regenerate.setStyleSheet("background-color: #95a5a6;")
        btn_regenerate.clicked.connect(self.generate_sample_plot)
        layout.addWidget(btn_regenerate)
        
        return panel
    
    def generate_sample_plot(self):
        """生成示例图形"""
        # 生成数据
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        
        self.x_data = np.linspace(0, 10, 100)
        
        # 多条曲线
        self.y_data = {}
        self.y_data['sin'] = np.sin(self.x_data) + np.random.randn(100) * 0.1
        self.y_data['cos'] = np.cos(self.x_data) + np.random.randn(100) * 0.1
        self.y_data['exp'] = np.exp(-self.x_data / 5) + np.random.randn(100) * 0.05
        
        # 绘图
        self.canvas.axes.clear()
        
        self.canvas.axes.plot(self.x_data, self.y_data['sin'], 'b-', 
                               linewidth=1.5, label=r'$\sin(x)$')
        self.canvas.axes.plot(self.x_data, self.y_data['cos'], 'r--', 
                               linewidth=1.5, label=r'$\cos(x)$')
        self.canvas.axes.plot(self.x_data, self.y_data['exp'], 'g-.', 
                               linewidth=1.5, label=r'$e^{-x/5}$')
        
        self.canvas.axes.set_xlabel('x', fontsize=12)
        self.canvas.axes.set_ylabel('y', fontsize=12)
        self.canvas.axes.set_title('示例图形 - 可导出为多种格式', fontsize=14)
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
        
        self.label_status.setText("已生成新的示例数据")
        self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")
    
    def save_image(self):
        """保存图片"""
        # 获取格式
        format_map = {
            "PNG": ("png", "PNG图片 (*.png)"),
            "PDF": ("pdf", "PDF文档 (*.pdf)"),
            "SVG": ("svg", "SVG矢量图 (*.svg)"),
            "EPS": ("eps", "EPS文件 (*.eps)"),
            "JPEG": ("jpg", "JPEG图片 (*.jpg)"),
        }
        
        fmt_name = self.combo_format.currentText()
        fmt_ext, fmt_filter = format_map.get(fmt_name, ("png", "PNG图片 (*.png)"))
        
        # 文件对话框
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            f"plot.{fmt_ext}",
            fmt_filter
        )
        
        if not filename:
            return
        
        # 获取参数
        dpi = self.spin_dpi.value()
        width = self.spin_width.value()
        height = self.spin_height.value()
        transparent = self.check_transparent.isChecked()
        tight = self.check_tight.isChecked()
        
        try:
            # 临时调整图形大小
            original_size = self.canvas.fig.get_size_inches()
            self.canvas.fig.set_size_inches(width, height)
            
            # 保存
            save_kwargs = {
                'dpi': dpi,
                'transparent': transparent,
                'facecolor': self.canvas.fig.get_facecolor() if not transparent else 'none',
            }
            
            if tight:
                save_kwargs['bbox_inches'] = 'tight'
                save_kwargs['pad_inches'] = 0.1
            
            self.canvas.fig.savefig(filename, **save_kwargs)
            
            # 恢复原始大小
            self.canvas.fig.set_size_inches(original_size)
            self.canvas.draw()
            
            self.label_status.setText(f"✓ 已保存: {os.path.basename(filename)}")
            self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")
            
            # 显示文件信息
            file_size = os.path.getsize(filename) / 1024
            QMessageBox.information(
                self, "保存成功",
                f"文件已保存:\n{filename}\n\n"
                f"格式: {fmt_name}\n"
                f"分辨率: {dpi} dpi\n"
                f"尺寸: {width}\" × {height}\"\n"
                f"文件大小: {file_size:.1f} KB"
            )
            
        except Exception as e:
            self.label_status.setText(f"✗ 保存失败: {str(e)}")
            self.label_status.setStyleSheet("color: #e74c3c; padding: 5px;")
            QMessageBox.critical(self, "错误", f"保存失败:\n{str(e)}")
    
    def save_csv(self):
        """保存为CSV"""
        if self.x_data is None:
            QMessageBox.warning(self, "警告", "没有数据可导出")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出CSV",
            "data.csv",
            "CSV文件 (*.csv)"
        )
        
        if not filename:
            return
        
        try:
            # 构建数据数组
            data = np.column_stack([
                self.x_data,
                self.y_data['sin'],
                self.y_data['cos'],
                self.y_data['exp']
            ])
            
            # 保存
            header = "x,sin(x),cos(x),exp(-x/5)"
            np.savetxt(filename, data, delimiter=',', header=header, comments='')
            
            self.label_status.setText(f"✓ 数据已导出: {os.path.basename(filename)}")
            self.label_status.setStyleSheet("color: #27ae60; padding: 5px;")
            
            QMessageBox.information(
                self, "导出成功",
                f"数据已导出为CSV:\n{filename}\n\n"
                f"数据点数: {len(self.x_data)}\n"
                f"列: x, sin(x), cos(x), exp(-x/5)"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")
    
    def save_numpy(self):
        """保存为NumPy格式"""
        if self.x_data is None:
            QMessageBox.warning(self, "警告", "没有数据可导出")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出NumPy",
            "data.npz",
            "NumPy文件 (*.npz)"
        )
        
        if not filename:
            return
        
        try:
            np.savez(
                filename,
                x=self.x_data,
                sin=self.y_data['sin'],
                cos=self.y_data['cos'],
                exp=self.y_data['exp']
            )
            
            self.label_status.setText(f"✓ 数据已导出: {os.path.basename(filename)}")
            self.label_status.setStyleSheet("color: #9b59b6; padding: 5px;")
            
            QMessageBox.information(
                self, "导出成功",
                f"数据已导出为NumPy格式:\n{filename}\n\n"
                f"加载方式:\n"
                f"data = np.load('{os.path.basename(filename)}')\n"
                f"x = data['x']\n"
                f"y = data['sin']"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败:\n{str(e)}")
    
    def batch_export(self):
        """批量导出所有格式"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择保存目录"
        )
        
        if not folder:
            return
        
        prefix = self.input_prefix.text() or "plot"
        dpi = self.spin_dpi.value()
        
        formats = ['png', 'pdf', 'svg']
        success_count = 0
        
        try:
            for fmt in formats:
                filename = os.path.join(folder, f"{prefix}.{fmt}")
                self.canvas.fig.savefig(
                    filename,
                    dpi=dpi,
                    bbox_inches='tight',
                    pad_inches=0.1
                )
                success_count += 1
            
            # 同时导出CSV
            csv_file = os.path.join(folder, f"{prefix}_data.csv")
            data = np.column_stack([
                self.x_data,
                self.y_data['sin'],
                self.y_data['cos'],
                self.y_data['exp']
            ])
            np.savetxt(csv_file, data, delimiter=',', 
                       header="x,sin,cos,exp", comments='')
            
            self.label_status.setText(f"✓ 批量导出完成: {success_count + 1} 个文件")
            self.label_status.setStyleSheet("color: #e67e22; padding: 5px;")
            
            QMessageBox.information(
                self, "批量导出完成",
                f"已导出到: {folder}\n\n"
                f"文件列表:\n"
                f"  • {prefix}.png\n"
                f"  • {prefix}.pdf\n"
                f"  • {prefix}.svg\n"
                f"  • {prefix}_data.csv"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"批量导出失败:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    
    window = PlotExportDemo()
    window.show()
    
    print("=" * 50)
    print("图表导出与保存")
    print("=" * 50)
    print("支持的图片格式:")
    print("  - PNG: 位图格式，适合网页和屏幕显示")
    print("  - PDF: 矢量格式，适合论文插图")
    print("  - SVG: 矢量格式，适合网页和编辑")
    print("  - EPS: 矢量格式，适合LaTeX文档")
    print("\n数据导出:")
    print("  - CSV: 通用表格格式")
    print("  - NPZ: NumPy压缩格式")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

