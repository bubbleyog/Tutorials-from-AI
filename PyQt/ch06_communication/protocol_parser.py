"""
示例程序：数据解析与协议
所属章节：第六章 - 仪器通信基础

功能说明：
    演示数据解析与协议处理：
    - ASCII数据解析
    - 二进制数据解析
    - 帧协议构建与解析
    - 校验和计算

运行方式：
    python protocol_parser.py
"""

import sys
import struct
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QGroupBox, QFormLayout,
    QComboBox, QTabWidget, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt


class ProtocolParserDemo(QMainWindow):
    """协议解析演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("数据解析与协议")
        self.setMinimumSize(800, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 使用标签页
        tabs = QTabWidget()
        tabs.addTab(self.create_ascii_tab(), "ASCII解析")
        tabs.addTab(self.create_binary_tab(), "二进制解析")
        tabs.addTab(self.create_frame_tab(), "帧协议")
        tabs.addTab(self.create_checksum_tab(), "校验和")
        
        main_layout.addWidget(tabs)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2ecc71;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #27ae60;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #27ae60; }
            QLineEdit, QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 2px solid #2ecc71;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #2ecc71;
                color: white;
            }
        """)
    
    def create_ascii_tab(self) -> QWidget:
        """ASCII解析标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区
        input_group = QGroupBox("输入数据")
        input_layout = QVBoxLayout()
        
        self.ascii_input = QLineEdit()
        self.ascii_input.setPlaceholderText("输入ASCII数据，如: T=300.5K 或 1.0,2.5,3.7")
        input_layout.addWidget(self.ascii_input)
        
        # 示例按钮
        example_layout = QHBoxLayout()
        examples = [
            ("温度", "T=300.5K"),
            ("CSV", "1.0,2.5,3.7,4.2"),
            ("键值对", "VOLT=1.234;CURR=0.056;FREQ=1000"),
            ("科学计数", "1.23E-5,4.56E+3"),
        ]
        for name, data in examples:
            btn = QPushButton(name)
            btn.clicked.connect(lambda c, d=data: self.ascii_input.setText(d))
            example_layout.addWidget(btn)
        input_layout.addLayout(example_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 解析选项
        options_layout = QHBoxLayout()
        
        options_layout.addWidget(QLabel("解析模式:"))
        self.ascii_mode = QComboBox()
        self.ascii_mode.addItems(["自动检测", "单值", "CSV", "键值对", "正则表达式"])
        options_layout.addWidget(self.ascii_mode)
        
        options_layout.addWidget(QLabel("分隔符:"))
        self.ascii_delimiter = QLineEdit(",")
        self.ascii_delimiter.setFixedWidth(50)
        options_layout.addWidget(self.ascii_delimiter)
        
        options_layout.addStretch()
        
        btn_parse = QPushButton("解析")
        btn_parse.clicked.connect(self.parse_ascii)
        options_layout.addWidget(btn_parse)
        
        layout.addLayout(options_layout)
        
        # 结果
        result_group = QGroupBox("解析结果")
        result_layout = QVBoxLayout()
        self.ascii_result = QTextEdit()
        self.ascii_result.setReadOnly(True)
        self.ascii_result.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        result_layout.addWidget(self.ascii_result)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        return tab
    
    def create_binary_tab(self) -> QWidget:
        """二进制解析标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区
        input_group = QGroupBox("输入数据 (HEX)")
        input_layout = QVBoxLayout()
        
        self.binary_input = QLineEdit()
        self.binary_input.setPlaceholderText("输入十六进制数据，如: 00 00 80 3F")
        input_layout.addWidget(self.binary_input)
        
        # 示例
        example_layout = QHBoxLayout()
        examples = [
            ("float=1.0", "00 00 80 3F"),
            ("int16=256", "00 01"),
            ("多个float", "00 00 80 3F 00 00 00 40 00 00 40 40"),
            ("混合数据", "01 00 64 00 00 80 3F"),
        ]
        for name, data in examples:
            btn = QPushButton(name)
            btn.clicked.connect(lambda c, d=data: self.binary_input.setText(d))
            example_layout.addWidget(btn)
        input_layout.addLayout(example_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 解析选项
        options_group = QGroupBox("解析选项")
        options_layout = QFormLayout()
        
        self.binary_format = QComboBox()
        self.binary_format.addItems([
            "float (4字节)",
            "double (8字节)",
            "int16 (2字节)",
            "int32 (4字节)",
            "uint16 (2字节)",
            "uint32 (4字节)",
            "自定义格式"
        ])
        options_layout.addRow("数据类型:", self.binary_format)
        
        self.binary_endian = QComboBox()
        self.binary_endian.addItems(["小端 (Little)", "大端 (Big)"])
        options_layout.addRow("字节序:", self.binary_endian)
        
        self.binary_custom = QLineEdit("<fff")
        self.binary_custom.setPlaceholderText("struct格式，如 <fff 表示3个小端float")
        options_layout.addRow("自定义格式:", self.binary_custom)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        btn_parse = QPushButton("解析")
        btn_parse.clicked.connect(self.parse_binary)
        layout.addWidget(btn_parse)
        
        # 结果
        result_group = QGroupBox("解析结果")
        result_layout = QVBoxLayout()
        self.binary_result = QTextEdit()
        self.binary_result.setReadOnly(True)
        self.binary_result.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        result_layout.addWidget(self.binary_result)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        return tab
    
    def create_frame_tab(self) -> QWidget:
        """帧协议标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 协议说明
        info = QLabel(
            "帧结构: [帧头 0xAA] [长度 1字节] [数据 N字节] [校验 1字节] [帧尾 0x55]"
        )
        info.setStyleSheet("""
            background-color: #e8f4f8;
            padding: 10px;
            border-radius: 5px;
        """)
        layout.addWidget(info)
        
        # 构建帧
        build_group = QGroupBox("构建数据帧")
        build_layout = QVBoxLayout()
        
        data_layout = QHBoxLayout()
        data_layout.addWidget(QLabel("数据 (HEX):"))
        self.frame_data = QLineEdit("01 02 03 04")
        data_layout.addWidget(self.frame_data)
        
        btn_build = QPushButton("构建帧")
        btn_build.clicked.connect(self.build_frame)
        data_layout.addWidget(btn_build)
        build_layout.addLayout(data_layout)
        
        self.frame_built = QLineEdit()
        self.frame_built.setReadOnly(True)
        self.frame_built.setStyleSheet("background-color: #f0f0f0;")
        build_layout.addWidget(self.frame_built)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        # 解析帧
        parse_group = QGroupBox("解析数据帧")
        parse_layout = QVBoxLayout()
        
        frame_layout = QHBoxLayout()
        frame_layout.addWidget(QLabel("帧数据 (HEX):"))
        self.frame_input = QLineEdit("AA 04 01 02 03 04 04 55")
        frame_layout.addWidget(self.frame_input)
        
        btn_parse_frame = QPushButton("解析帧")
        btn_parse_frame.clicked.connect(self.parse_frame)
        frame_layout.addWidget(btn_parse_frame)
        parse_layout.addLayout(frame_layout)
        
        self.frame_result = QTextEdit()
        self.frame_result.setReadOnly(True)
        self.frame_result.setMaximumHeight(150)
        self.frame_result.setStyleSheet("""
            font-family: Consolas, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        parse_layout.addWidget(self.frame_result)
        
        parse_group.setLayout(parse_layout)
        layout.addWidget(parse_group)
        
        layout.addStretch()
        
        return tab
    
    def create_checksum_tab(self) -> QWidget:
        """校验和标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入
        input_group = QGroupBox("输入数据 (HEX)")
        input_layout = QVBoxLayout()
        
        self.checksum_input = QLineEdit("01 02 03 04 05")
        input_layout.addWidget(self.checksum_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 计算按钮
        btn_calc = QPushButton("计算校验和")
        btn_calc.clicked.connect(self.calculate_checksums)
        layout.addWidget(btn_calc)
        
        # 结果
        result_group = QGroupBox("校验和结果")
        result_layout = QFormLayout()
        
        self.checksum_sum = QLineEdit()
        self.checksum_sum.setReadOnly(True)
        result_layout.addRow("累加和 (SUM):", self.checksum_sum)
        
        self.checksum_xor = QLineEdit()
        self.checksum_xor.setReadOnly(True)
        result_layout.addRow("异或 (XOR):", self.checksum_xor)
        
        self.checksum_crc8 = QLineEdit()
        self.checksum_crc8.setReadOnly(True)
        result_layout.addRow("CRC-8:", self.checksum_crc8)
        
        self.checksum_crc16 = QLineEdit()
        self.checksum_crc16.setReadOnly(True)
        result_layout.addRow("CRC-16 (Modbus):", self.checksum_crc16)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # 说明
        info_group = QGroupBox("校验和算法说明")
        info_layout = QVBoxLayout()
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setText("""
累加和 (SUM):
  - 将所有字节相加，取低8位
  - 公式: sum(data) & 0xFF

异或 (XOR):
  - 将所有字节异或
  - 公式: data[0] ^ data[1] ^ ... ^ data[n]

CRC-8:
  - 多项式: 0x07 (x^8 + x^2 + x + 1)
  - 初始值: 0x00

CRC-16 (Modbus):
  - 多项式: 0xA001 (反转后)
  - 初始值: 0xFFFF
        """)
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        return tab
    
    # ========== ASCII解析 ==========
    
    def parse_ascii(self):
        """解析ASCII数据"""
        text = self.ascii_input.text().strip()
        if not text:
            return
        
        mode = self.ascii_mode.currentIndex()
        delimiter = self.ascii_delimiter.text()
        
        result = []
        result.append(f"输入: {text}")
        result.append("-" * 40)
        
        try:
            if mode == 0:  # 自动检测
                # 尝试不同的解析方式
                if '=' in text and ';' in text:
                    # 键值对
                    pairs = text.split(';')
                    result.append("检测到: 键值对格式")
                    for pair in pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            result.append(f"  {key.strip()} = {value.strip()}")
                elif '=' in text:
                    # 单个键值对
                    match = re.match(r'([A-Za-z]+)=([0-9.eE+-]+)([A-Za-z]*)', text)
                    if match:
                        result.append("检测到: 带单位的值")
                        result.append(f"  变量: {match.group(1)}")
                        result.append(f"  数值: {match.group(2)}")
                        result.append(f"  单位: {match.group(3) or '无'}")
                elif ',' in text:
                    # CSV
                    values = [float(x) for x in text.split(',')]
                    result.append("检测到: CSV格式")
                    for i, v in enumerate(values):
                        result.append(f"  [{i}] = {v}")
                else:
                    # 单值
                    value = float(text)
                    result.append(f"检测到: 单个数值 = {value}")
                    
            elif mode == 1:  # 单值
                value = float(text)
                result.append(f"解析结果: {value}")
                
            elif mode == 2:  # CSV
                values = [float(x) for x in text.split(delimiter)]
                result.append(f"解析到 {len(values)} 个值:")
                for i, v in enumerate(values):
                    result.append(f"  [{i}] = {v}")
                    
            elif mode == 3:  # 键值对
                pairs = text.split(';')
                result.append(f"解析到 {len(pairs)} 个键值对:")
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        result.append(f"  {key.strip()} = {value.strip()}")
                        
        except Exception as e:
            result.append(f"解析错误: {e}")
        
        self.ascii_result.setText('\n'.join(result))
    
    # ========== 二进制解析 ==========
    
    def parse_binary(self):
        """解析二进制数据"""
        hex_str = self.binary_input.text().replace(' ', '')
        if not hex_str:
            return
        
        try:
            data = bytes.fromhex(hex_str)
        except ValueError as e:
            self.binary_result.setText(f"HEX格式错误: {e}")
            return
        
        format_idx = self.binary_format.currentIndex()
        endian = '<' if self.binary_endian.currentIndex() == 0 else '>'
        
        result = []
        result.append(f"原始数据: {' '.join(f'{b:02X}' for b in data)}")
        result.append(f"长度: {len(data)} 字节")
        result.append("-" * 40)
        
        try:
            if format_idx == 6:  # 自定义格式
                fmt = self.binary_custom.text()
                values = struct.unpack(fmt, data)
                result.append(f"格式: {fmt}")
                for i, v in enumerate(values):
                    result.append(f"  [{i}] = {v}")
            else:
                # 预定义格式
                formats = {
                    0: ('f', 4, 'float'),
                    1: ('d', 8, 'double'),
                    2: ('h', 2, 'int16'),
                    3: ('i', 4, 'int32'),
                    4: ('H', 2, 'uint16'),
                    5: ('I', 4, 'uint32'),
                }
                fmt_char, size, type_name = formats[format_idx]
                
                count = len(data) // size
                fmt = endian + fmt_char * count
                
                if len(data) >= size:
                    values = struct.unpack(fmt, data[:count*size])
                    result.append(f"类型: {type_name}")
                    result.append(f"解析到 {len(values)} 个值:")
                    for i, v in enumerate(values):
                        result.append(f"  [{i}] = {v}")
                else:
                    result.append(f"数据长度不足，需要至少 {size} 字节")
                    
        except Exception as e:
            result.append(f"解析错误: {e}")
        
        self.binary_result.setText('\n'.join(result))
    
    # ========== 帧协议 ==========
    
    def build_frame(self):
        """构建数据帧"""
        hex_str = self.frame_data.text().replace(' ', '')
        if not hex_str:
            return
        
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            self.frame_built.setText("HEX格式错误")
            return
        
        # 构建帧
        length = len(data)
        checksum = 0
        for b in data:
            checksum ^= b
        
        frame = bytes([0xAA, length]) + data + bytes([checksum, 0x55])
        
        self.frame_built.setText(' '.join(f'{b:02X}' for b in frame))
    
    def parse_frame(self):
        """解析数据帧"""
        hex_str = self.frame_input.text().replace(' ', '')
        if not hex_str:
            return
        
        try:
            frame = bytes.fromhex(hex_str)
        except ValueError:
            self.frame_result.setText("HEX格式错误")
            return
        
        result = []
        result.append(f"帧数据: {' '.join(f'{b:02X}' for b in frame)}")
        result.append("-" * 40)
        
        # 检查帧头帧尾
        if len(frame) < 4:
            result.append("错误: 帧长度不足")
        elif frame[0] != 0xAA:
            result.append(f"错误: 帧头错误 (期望 0xAA, 实际 0x{frame[0]:02X})")
        elif frame[-1] != 0x55:
            result.append(f"错误: 帧尾错误 (期望 0x55, 实际 0x{frame[-1]:02X})")
        else:
            length = frame[1]
            data = frame[2:2+length]
            checksum = frame[2+length]
            
            # 计算校验和
            calc_checksum = 0
            for b in data:
                calc_checksum ^= b
            
            result.append(f"帧头: 0x{frame[0]:02X} ✓")
            result.append(f"长度: {length}")
            result.append(f"数据: {' '.join(f'{b:02X}' for b in data)}")
            result.append(f"校验: 0x{checksum:02X} (计算值: 0x{calc_checksum:02X})")
            result.append(f"帧尾: 0x{frame[-1]:02X} ✓")
            
            if checksum == calc_checksum:
                result.append("\n✓ 帧校验通过")
            else:
                result.append("\n✗ 帧校验失败")
        
        self.frame_result.setText('\n'.join(result))
    
    # ========== 校验和 ==========
    
    def calculate_checksums(self):
        """计算各种校验和"""
        hex_str = self.checksum_input.text().replace(' ', '')
        if not hex_str:
            return
        
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            self.checksum_sum.setText("HEX格式错误")
            return
        
        # 累加和
        sum_val = sum(data) & 0xFF
        self.checksum_sum.setText(f"0x{sum_val:02X} ({sum_val})")
        
        # 异或
        xor_val = 0
        for b in data:
            xor_val ^= b
        self.checksum_xor.setText(f"0x{xor_val:02X} ({xor_val})")
        
        # CRC-8
        crc8 = self.calc_crc8(data)
        self.checksum_crc8.setText(f"0x{crc8:02X} ({crc8})")
        
        # CRC-16 Modbus
        crc16 = self.calc_crc16(data)
        self.checksum_crc16.setText(f"0x{crc16:04X} ({crc16})")
    
    def calc_crc8(self, data: bytes) -> int:
        """计算CRC-8"""
        crc = 0x00
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x07
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc
    
    def calc_crc16(self, data: bytes) -> int:
        """计算CRC-16 (Modbus)"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc


def main():
    app = QApplication(sys.argv)
    window = ProtocolParserDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

