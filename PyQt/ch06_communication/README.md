# 第六章：仪器通信基础

> 本章将学习与实验仪器通信的基础知识，包括串口、网络和VISA协议

## 本章内容

- [6.1 串口通信基础](#61-串口通信基础)
- [6.2 串口数据收发](#62-串口数据收发)
- [6.3 网络通信TCP/UDP](#63-网络通信tcpudp)
- [6.4 VISA仪器控制](#64-visa仪器控制)
- [6.5 数据解析与协议](#65-数据解析与协议)

---

## 前置准备

### 安装通信库

```bash
pip install pyserial pyvisa pyvisa-py
```

### 常用仪器接口

| 接口类型 | 特点 | 典型应用 |
|----------|------|----------|
| RS-232/485 | 简单可靠，距离短 | 温控器、电源、万用表 |
| USB-TMC | 即插即用 | 示波器、信号发生器 |
| GPIB | 高速可靠 | 老式高端仪器 |
| LAN/Ethernet | 远程控制 | 现代仪器 |

---

## 6.1 串口通信基础

**示例程序**：[serial_basic.py](serial_basic.py)

### pyserial 基本用法

```python
import serial

# 打开串口
ser = serial.Serial(
    port='COM3',        # 或 '/dev/ttyUSB0' (Linux)
    baudrate=9600,      # 波特率
    bytesize=8,         # 数据位
    parity='N',         # 校验位: N-无, E-偶, O-奇
    stopbits=1,         # 停止位
    timeout=1           # 读取超时(秒)
)

# 发送数据
ser.write(b'*IDN?\n')

# 接收数据
response = ser.readline()
print(response.decode('ascii'))

# 关闭串口
ser.close()
```

### 列出可用串口

```python
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")
```

### 串口参数说明

| 参数 | 常用值 | 说明 |
|------|--------|------|
| baudrate | 9600, 19200, 115200 | 通信速率 |
| bytesize | 8 | 数据位数 |
| parity | 'N', 'E', 'O' | 无/偶/奇校验 |
| stopbits | 1, 2 | 停止位 |
| timeout | 1.0 | 读取超时(秒) |

### 常见问题

1. **权限问题 (Linux)**
   ```bash
   sudo usermod -a -G dialout $USER
   # 重新登录生效
   ```

2. **串口占用**
   - 确保没有其他程序使用该串口
   - Windows: 设备管理器查看
   - Linux: `lsof /dev/ttyUSB0`

---

## 6.2 串口数据收发

**示例程序**：[serial_comm.py](serial_comm.py)

### 在PyQt中使用串口

关键：**使用QThread进行串口读取，避免阻塞GUI**

```python
from PyQt6.QtCore import QThread, pyqtSignal
import serial

class SerialReader(QThread):
    """串口读取线程"""
    
    data_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, port: str, baudrate: int):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.serial = None
    
    def run(self):
        try:
            self.serial = serial.Serial(
                self.port, 
                self.baudrate, 
                timeout=0.1
            )
            self.running = True
            
            while self.running:
                if self.serial.in_waiting:
                    data = self.serial.readline()
                    self.data_received.emit(data)
                    
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if self.serial:
                self.serial.close()
    
    def stop(self):
        self.running = False
        self.wait()
    
    def send(self, data: bytes):
        if self.serial and self.serial.is_open:
            self.serial.write(data)
```

### 连接到GUI

```python
class MainWindow(QMainWindow):
    def connect_serial(self):
        self.reader = SerialReader('COM3', 9600)
        self.reader.data_received.connect(self.on_data_received)
        self.reader.error_occurred.connect(self.on_error)
        self.reader.start()
    
    def on_data_received(self, data: bytes):
        text = data.decode('ascii', errors='replace')
        self.text_log.append(text)
    
    def send_command(self, cmd: str):
        self.reader.send(cmd.encode('ascii') + b'\n')
```

---

## 6.3 网络通信TCP/UDP

**示例程序**：[network_comm.py](network_comm.py)

### TCP客户端

```python
import socket

def tcp_query(host: str, port: int, command: str) -> str:
    """TCP查询"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.settimeout(5.0)
        
        # 发送命令
        sock.sendall(command.encode('ascii') + b'\n')
        
        # 接收响应
        response = sock.recv(4096)
        return response.decode('ascii')
```

### UDP通信

```python
def udp_send(host: str, port: int, data: bytes):
    """UDP发送"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data, (host, port))
```

### PyQt中的网络通信

使用 `QTcpSocket` 进行异步网络通信：

```python
from PyQt6.QtNetwork import QTcpSocket, QHostAddress

class NetworkClient(QObject):
    def __init__(self):
        super().__init__()
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.on_connected)
        self.socket.readyRead.connect(self.on_data_ready)
        self.socket.errorOccurred.connect(self.on_error)
    
    def connect_to_host(self, host: str, port: int):
        self.socket.connectToHost(host, port)
    
    def on_connected(self):
        print("已连接")
    
    def on_data_ready(self):
        data = self.socket.readAll().data()
        print(f"收到: {data}")
    
    def send(self, data: bytes):
        self.socket.write(data)
```

---

## 6.4 VISA仪器控制

**示例程序**：[visa_control.py](visa_control.py)

### VISA简介

VISA (Virtual Instrument Software Architecture) 是仪器控制的标准接口，支持：
- GPIB
- USB-TMC
- VXI
- LAN
- RS-232

### PyVISA基本用法

```python
import pyvisa

# 创建资源管理器
rm = pyvisa.ResourceManager()

# 列出所有仪器
resources = rm.list_resources()
print(resources)  # ('USB0::0x1AB1::0x0588::...', ...)

# 连接仪器
inst = rm.open_resource('USB0::0x1AB1::0x0588::DS1ZA123456789::INSTR')

# 查询仪器ID
idn = inst.query('*IDN?')
print(idn)

# 发送命令
inst.write(':CHAN1:DISP ON')

# 查询数据
data = inst.query(':MEAS:FREQ? CHAN1')

# 关闭连接
inst.close()
```

### 常用SCPI命令

| 命令 | 功能 |
|------|------|
| `*IDN?` | 查询仪器ID |
| `*RST` | 复位仪器 |
| `*OPC?` | 操作完成查询 |
| `*CLS` | 清除状态 |

### 示波器常用命令

```python
# Rigol DS1000Z 示例
inst.write(':RUN')          # 运行
inst.write(':STOP')         # 停止
inst.write(':SING')         # 单次触发

# 测量
freq = inst.query(':MEAS:FREQ? CHAN1')
vpp = inst.query(':MEAS:VPP? CHAN1')

# 获取波形数据
inst.write(':WAV:SOUR CHAN1')
inst.write(':WAV:MODE NORM')
inst.write(':WAV:FORM ASCII')
data = inst.query(':WAV:DATA?')
```

### 电源控制示例

```python
# Keithley 2400 源表
inst.write(':SOUR:FUNC VOLT')       # 电压源模式
inst.write(':SOUR:VOLT 1.5')        # 设置1.5V
inst.write(':SENS:FUNC "CURR"')     # 测量电流
inst.write(':OUTP ON')              # 输出开
current = inst.query(':MEAS:CURR?') # 读取电流
```

---

## 6.5 数据解析与协议

**示例程序**：[protocol_parser.py](protocol_parser.py)

### 常见数据格式

#### ASCII格式
```
# 简单数值
"123.456\r\n"

# 带单位
"T=300.5K\r\n"

# CSV格式
"1.0,2.5,3.7\r\n"
```

#### 二进制格式
```python
import struct

# 解析32位浮点数 (小端序)
data = b'\x00\x00\x80\x3f'  # 1.0
value = struct.unpack('<f', data)[0]

# 打包数据
packed = struct.pack('<ff', 1.0, 2.0)
```

### 数据解析示例

```python
def parse_temperature(response: str) -> float:
    """解析温度响应: 'T=300.5K'"""
    match = re.match(r'T=([0-9.]+)K', response)
    if match:
        return float(match.group(1))
    raise ValueError(f"无法解析: {response}")

def parse_csv_data(response: str) -> list:
    """解析CSV数据"""
    return [float(x) for x in response.strip().split(',')]
```

### 校验和计算

```python
def checksum_xor(data: bytes) -> int:
    """XOR校验和"""
    result = 0
    for byte in data:
        result ^= byte
    return result

def checksum_sum(data: bytes) -> int:
    """累加校验和"""
    return sum(data) & 0xFF

def crc16(data: bytes) -> int:
    """CRC-16校验"""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc
```

### 帧协议示例

```
帧结构:
+------+------+--------+------+------+
| 帧头 | 长度 | 数据   | 校验 | 帧尾 |
| 0xAA | 1字节| N字节  | 1字节| 0x55 |
+------+------+--------+------+------+
```

```python
def build_frame(data: bytes) -> bytes:
    """构建数据帧"""
    length = len(data)
    checksum = checksum_xor(data)
    return bytes([0xAA, length]) + data + bytes([checksum, 0x55])

def parse_frame(frame: bytes) -> bytes:
    """解析数据帧"""
    if frame[0] != 0xAA or frame[-1] != 0x55:
        raise ValueError("帧格式错误")
    
    length = frame[1]
    data = frame[2:2+length]
    checksum = frame[2+length]
    
    if checksum_xor(data) != checksum:
        raise ValueError("校验和错误")
    
    return data
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **串口通信**：pyserial的使用、参数配置、多线程读取
2. **网络通信**：TCP/UDP客户端、QTcpSocket
3. **VISA控制**：PyVISA、SCPI命令、常用仪器控制
4. **数据解析**：ASCII/二进制解析、校验和、帧协议

### 仪器通信架构

```
┌─────────────────────────────────────────────┐
│              PyQt GUI 主线程                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ 控制面板 │  │ 数据显示 │  │ 图形绑制 │     │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │            │            │          │
│  ╔════╧════════════╧════════════╧════╗     │
│  ║         信号/槽通信              ║     │
│  ╚════╤════════════╤════════════╤════╝     │
└───────┼────────────┼────────────┼──────────┘
        │            │            │
┌───────┴────┐ ┌─────┴─────┐ ┌────┴─────┐
│  通信线程   │ │  通信线程  │ │  通信线程 │
│  (串口)    │ │  (网络)   │ │  (VISA)  │
└─────┬──────┘ └─────┬─────┘ └────┬─────┘
      │              │            │
┌─────┴──────┐ ┌─────┴─────┐ ┌────┴─────┐
│  温控器    │ │  数据采集  │ │  示波器   │
│  RS-485   │ │  TCP/IP   │ │  USB-TMC │
└────────────┘ └───────────┘ └──────────┘
```

### 练习题

1. 编写一个串口调试助手：
   - 支持选择串口和配置参数
   - 显示收发数据（HEX/ASCII）
   - 支持定时发送

2. 创建一个VISA仪器扫描器：
   - 列出所有可用仪器
   - 自动查询*IDN?
   - 保存仪器信息

---

## 下一章预告

[第七章：仪器控制界面实战](../ch07_instrument/) - 整合所有知识，创建完整的仪器控制界面。

