"""
示例程序：表格控件显示数据
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示QTableWidget的使用：
    - 创建和填充表格
    - 从NumPy数组加载数据
    - 表格样式和选择模式
    - 数据编辑和导出

运行方式：
    python table_view.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QComboBox,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush


class TableViewDemo(QMainWindow):
    """表格控件演示"""
    
    def __init__(self):
        super().__init__()
        self.data = None
        self.init_ui()
        self.generate_sample_data()
    
    def init_ui(self):
        self.setWindowTitle("表格控件 - 数据显示与编辑")
        self.setMinimumSize(900, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        
        # 数据生成
        gen_group = QGroupBox("生成数据")
        gen_layout = QFormLayout()
        
        self.spin_rows = QSpinBox()
        self.spin_rows.setRange(5, 1000)
        self.spin_rows.setValue(20)
        gen_layout.addRow("行数:", self.spin_rows)
        
        self.spin_cols = QSpinBox()
        self.spin_cols.setRange(2, 10)
        self.spin_cols.setValue(5)
        gen_layout.addRow("列数:", self.spin_cols)
        
        self.combo_data_type = QComboBox()
        self.combo_data_type.addItems(["随机数据", "正弦波", "实验数据模拟"])
        gen_layout.addRow("数据类型:", self.combo_data_type)
        
        btn_generate = QPushButton("生成数据")
        btn_generate.clicked.connect(self.generate_sample_data)
        gen_layout.addRow("", btn_generate)
        
        gen_group.setLayout(gen_layout)
        left_layout.addWidget(gen_group)
        
        # 显示选项
        display_group = QGroupBox("显示选项")
        display_layout = QVBoxLayout()
        
        btn_auto_resize = QPushButton("自动调整列宽")
        btn_auto_resize.clicked.connect(self.auto_resize_columns)
        display_layout.addWidget(btn_auto_resize)
        
        btn_highlight = QPushButton("高亮最大/最小值")
        btn_highlight.clicked.connect(self.highlight_extremes)
        display_layout.addWidget(btn_highlight)
        
        btn_clear_highlight = QPushButton("清除高亮")
        btn_clear_highlight.clicked.connect(self.clear_highlight)
        display_layout.addWidget(btn_clear_highlight)
        
        display_group.setLayout(display_layout)
        left_layout.addWidget(display_group)
        
        # 数据操作
        ops_group = QGroupBox("数据操作")
        ops_layout = QVBoxLayout()
        
        btn_add_row = QPushButton("添加行")
        btn_add_row.clicked.connect(self.add_row)
        ops_layout.addWidget(btn_add_row)
        
        btn_delete_row = QPushButton("删除选中行")
        btn_delete_row.clicked.connect(self.delete_selected_rows)
        ops_layout.addWidget(btn_delete_row)
        
        btn_sort = QPushButton("按第一列排序")
        btn_sort.clicked.connect(self.sort_by_first_column)
        ops_layout.addWidget(btn_sort)
        
        ops_group.setLayout(ops_layout)
        left_layout.addWidget(ops_group)
        
        # 导入导出
        io_group = QGroupBox("导入/导出")
        io_layout = QVBoxLayout()
        
        btn_import = QPushButton("📂 导入CSV")
        btn_import.clicked.connect(self.import_csv)
        io_layout.addWidget(btn_import)
        
        btn_export = QPushButton("💾 导出CSV")
        btn_export.clicked.connect(self.export_csv)
        io_layout.addWidget(btn_export)
        
        io_group.setLayout(io_layout)
        left_layout.addWidget(io_group)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel)
        
        # 右侧表格区域
        right_layout = QVBoxLayout()
        
        # 统计信息
        self.label_info = QLabel("数据: 0 行 × 0 列")
        self.label_info.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        right_layout.addWidget(self.label_info)
        
        # 表格
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        
        # 表格样式
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                font-size: 12px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: 1px solid #2c3e50;
                font-weight: bold;
            }
        """)
        
        right_layout.addWidget(self.table)
        
        # 选中信息
        self.label_selection = QLabel("选中: 无")
        self.label_selection.setStyleSheet("color: #7f8c8d; padding: 5px;")
        right_layout.addWidget(self.label_selection)
        
        main_layout.addLayout(right_layout)
        
        # 连接选择变化信号
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # 窗口样式
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
            }
            QPushButton {
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
    
    def generate_sample_data(self):
        """生成示例数据"""
        rows = self.spin_rows.value()
        cols = self.spin_cols.value()
        data_type = self.combo_data_type.currentIndex()
        
        if data_type == 0:  # 随机数据
            self.data = np.random.randn(rows, cols)
            headers = [f"随机{i+1}" for i in range(cols)]
            
        elif data_type == 1:  # 正弦波
            x = np.linspace(0, 4 * np.pi, rows)
            self.data = np.column_stack([
                x,
                np.sin(x),
                np.cos(x),
                np.sin(2*x),
                np.exp(-x/10)
            ])[:, :cols]
            headers = ["x", "sin(x)", "cos(x)", "sin(2x)", "exp(-x/10)"][:cols]
            
        else:  # 实验数据模拟
            time = np.arange(rows) * 0.1
            temp = 300 + 50 * (1 - np.exp(-time/5)) + np.random.randn(rows) * 2
            voltage = 1.5 + 0.01 * temp + np.random.randn(rows) * 0.05
            current = voltage / 100 + np.random.randn(rows) * 0.001
            power = voltage * current
            resistance = voltage / current
            
            self.data = np.column_stack([time, temp, voltage, current, power])[:, :cols]
            headers = ["时间(s)", "温度(K)", "电压(V)", "电流(A)", "功率(W)"][:cols]
        
        self.load_data_to_table(self.data, headers)
    
    def load_data_to_table(self, data: np.ndarray, headers: list):
        """将NumPy数组加载到表格"""
        rows, cols = data.shape
        
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels(headers)
        
        for i in range(rows):
            for j in range(cols):
                value = data[i, j]
                item = QTableWidgetItem(f"{value:.6g}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, j, item)
        
        self.label_info.setText(f"数据: {rows} 行 × {cols} 列")
        self.auto_resize_columns()
    
    def auto_resize_columns(self):
        """自动调整列宽"""
        self.table.resizeColumnsToContents()
        
        # 设置最小宽度
        for i in range(self.table.columnCount()):
            if self.table.columnWidth(i) < 80:
                self.table.setColumnWidth(i, 80)
    
    def highlight_extremes(self):
        """高亮最大最小值"""
        if self.data is None:
            return
        
        for j in range(self.table.columnCount()):
            col_data = self.data[:, j]
            max_idx = np.argmax(col_data)
            min_idx = np.argmin(col_data)
            
            # 高亮最大值（红色）
            max_item = self.table.item(max_idx, j)
            if max_item:
                max_item.setBackground(QBrush(QColor("#ffcccc")))
                max_item.setForeground(QBrush(QColor("#c0392b")))
            
            # 高亮最小值（蓝色）
            min_item = self.table.item(min_idx, j)
            if min_item:
                min_item.setBackground(QBrush(QColor("#cce5ff")))
                min_item.setForeground(QBrush(QColor("#2980b9")))
    
    def clear_highlight(self):
        """清除高亮"""
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item:
                    item.setBackground(QBrush(QColor("white")))
                    item.setForeground(QBrush(QColor("black")))
    
    def add_row(self):
        """添加行"""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        
        for j in range(self.table.columnCount()):
            item = QTableWidgetItem("0")
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_count, j, item)
        
        self.label_info.setText(f"数据: {self.table.rowCount()} 行 × {self.table.columnCount()} 列")
    
    def delete_selected_rows(self):
        """删除选中的行"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
        
        self.label_info.setText(f"数据: {self.table.rowCount()} 行 × {self.table.columnCount()} 列")
    
    def sort_by_first_column(self):
        """按第一列排序"""
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def on_selection_changed(self):
        """选择变化时更新信息"""
        selected = self.table.selectedItems()
        if not selected:
            self.label_selection.setText("选中: 无")
            return
        
        # 获取选中的行
        rows = set(item.row() for item in selected)
        
        # 计算选中数据的统计
        values = []
        for item in selected:
            try:
                values.append(float(item.text()))
            except:
                pass
        
        if values:
            info = f"选中 {len(rows)} 行 | "
            info += f"平均: {np.mean(values):.4g} | "
            info += f"总和: {np.sum(values):.4g}"
            self.label_selection.setText(info)
        else:
            self.label_selection.setText(f"选中 {len(rows)} 行")
    
    def import_csv(self):
        """导入CSV"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "导入CSV", "", "CSV文件 (*.csv);;所有文件 (*)"
        )
        
        if filename:
            try:
                self.data = np.loadtxt(filename, delimiter=',', skiprows=1)
                cols = self.data.shape[1]
                headers = [f"列{i+1}" for i in range(cols)]
                self.load_data_to_table(self.data, headers)
                
            except Exception as e:
                QMessageBox.critical(self, "导入错误", str(e))
    
    def export_csv(self):
        """导出CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出CSV", "data.csv", "CSV文件 (*.csv)"
        )
        
        if filename:
            try:
                rows = self.table.rowCount()
                cols = self.table.columnCount()
                
                # 获取表头
                headers = []
                for j in range(cols):
                    header = self.table.horizontalHeaderItem(j)
                    headers.append(header.text() if header else f"列{j+1}")
                
                # 获取数据
                data = []
                for i in range(rows):
                    row_data = []
                    for j in range(cols):
                        item = self.table.item(i, j)
                        row_data.append(float(item.text()) if item else 0)
                    data.append(row_data)
                
                data = np.array(data)
                np.savetxt(filename, data, delimiter=',', 
                          header=','.join(headers), comments='')
                
                QMessageBox.information(self, "导出成功", f"已导出到:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "导出错误", str(e))


def main():
    app = QApplication(sys.argv)
    window = TableViewDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

