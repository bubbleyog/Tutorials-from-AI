# 第七章：仪器控制界面实战

> 本章整合前面所学知识，创建完整的仪器控制界面

## 本章内容

- [7.1 温度控制器界面](#71-温度控制器界面)
- [7.2 信号发生器控制](#72-信号发生器控制)
- [7.3 数据采集系统](#73-数据采集系统)
- [7.4 完整仪器控制框架](#74-完整仪器控制框架)

---

## 设计原则

在开发仪器控制界面时，应遵循以下原则：

### 1. 分离关注点

```
┌─────────────────────────────────────────────┐
│                  GUI层                       │
│  (显示、用户交互、信号槽)                     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                控制层                        │
│  (业务逻辑、状态管理、数据处理)               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│               通信层                         │
│  (串口/网络/VISA、协议解析)                  │
└─────────────────────────────────────────────┘
```

### 2. 线程安全

- GUI操作只在主线程
- 通信操作放在工作线程
- 使用信号槽进行线程间通信

### 3. 状态管理

```python
class InstrumentState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    RUNNING = 3
    ERROR = 4
```

### 4. 错误处理

- 通信超时处理
- 异常值检测
- 用户友好的错误提示

---

## 7.1 温度控制器界面

**示例程序**：[temperature_controller.py](temperature_controller.py)

### 功能需求

1. **连接管理**
   - 串口/网络连接配置
   - 连接状态显示

2. **温度显示**
   - 当前温度实时显示
   - 设定温度输入
   - 温度历史曲线

3. **控制功能**
   - PID参数设置
   - 升温/降温控制
   - 紧急停止

4. **数据记录**
   - 温度数据保存
   - 日志记录

### 界面设计

```
┌────────────────────────────────────────────┐
│  温度控制器                          [_][□][×]│
├────────────────────────────────────────────┤
│ ┌──────────┐ ┌─────────────────────────────┐│
│ │连接设置   │ │      温度曲线图             ││
│ │ 端口 [▼] │ │                             ││
│ │ 波特率   │ │    ~~~~/\~~~~/\~~~~         ││
│ │[连接]    │ │                             ││
│ ├──────────┤ └─────────────────────────────┘│
│ │当前温度   │                               │
│ │ 298.5 K  │ ┌─────────────────────────────┐│
│ │设定温度   │ │  PID参数                    ││
│ │[  300  ] │ │  P: [___] I: [___] D: [___] ││
│ │[升温][停止]│ │  [应用]                    ││
│ └──────────┘ └─────────────────────────────┘│
├────────────────────────────────────────────┤
│ 状态: 已连接 | 温度稳定                      │
└────────────────────────────────────────────┘
```

### 关键代码

```python
class TemperatureController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_temp = 0
        self.target_temp = 300
        self.temp_history = []
        
    def update_temperature(self, temp: float):
        """更新温度显示"""
        self.current_temp = temp
        self.temp_history.append((time.time(), temp))
        
        # 更新显示
        self.label_temp.setText(f"{temp:.1f} K")
        
        # 更新曲线
        self.update_plot()
        
        # 检查是否到达目标
        if abs(temp - self.target_temp) < 0.5:
            self.label_status.setText("温度稳定")
```

---

## 7.2 信号发生器控制

**示例程序**：[signal_generator.py](signal_generator.py)

### 功能需求

1. **波形设置**
   - 波形类型（正弦、方波、三角波、锯齿波）
   - 频率、幅度、偏置
   - 占空比（方波）

2. **输出控制**
   - 输出开/关
   - 多通道切换

3. **波形预览**
   - 实时波形显示
   - 参数变化即时反馈

### 波形生成

```python
def generate_waveform(self, wave_type: str, freq: float, 
                      amp: float, offset: float, 
                      duty: float = 50) -> np.ndarray:
    t = np.linspace(0, 1/freq, 1000)
    
    if wave_type == "正弦波":
        y = amp * np.sin(2 * np.pi * freq * t) + offset
    elif wave_type == "方波":
        y = amp * signal.square(2 * np.pi * freq * t, duty/100) + offset
    elif wave_type == "三角波":
        y = amp * signal.sawtooth(2 * np.pi * freq * t, 0.5) + offset
    elif wave_type == "锯齿波":
        y = amp * signal.sawtooth(2 * np.pi * freq * t) + offset
    
    return t, y
```

---

## 7.3 数据采集系统

**示例程序**：[data_acquisition.py](data_acquisition.py)

### 功能需求

1. **多通道采集**
   - 配置采集通道
   - 采样率设置
   - 触发模式

2. **实时显示**
   - 多通道波形
   - 数值监控

3. **数据存储**
   - 连续记录
   - 触发记录
   - 文件格式选择

### 采集架构

```python
class DataAcquisitionThread(QThread):
    """数据采集线程"""
    
    data_ready = pyqtSignal(np.ndarray)
    
    def __init__(self, channels: int, sample_rate: float):
        super().__init__()
        self.channels = channels
        self.sample_rate = sample_rate
        self.running = False
    
    def run(self):
        self.running = True
        buffer_size = int(self.sample_rate * 0.1)  # 100ms缓冲
        
        while self.running:
            # 从硬件读取数据
            data = self.read_from_hardware(buffer_size)
            self.data_ready.emit(data)
            
    def read_from_hardware(self, size: int) -> np.ndarray:
        # 实际项目中这里连接DAQ硬件
        # 这里用模拟数据代替
        t = np.arange(size) / self.sample_rate
        data = np.zeros((self.channels, size))
        for i in range(self.channels):
            data[i] = np.sin(2 * np.pi * (i+1) * 10 * t)
        return data
```

---

## 7.4 完整仪器控制框架

**示例程序**：[instrument_framework.py](instrument_framework.py)

### 框架设计

```python
from abc import ABC, abstractmethod

class InstrumentBase(ABC):
    """仪器基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接仪器"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def query(self, command: str) -> str:
        """发送查询命令"""
        pass
    
    @abstractmethod
    def write(self, command: str):
        """发送写命令"""
        pass
    
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """是否已连接"""
        pass
```

### 仪器实现

```python
class SerialInstrument(InstrumentBase):
    """串口仪器"""
    
    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
    
    def connect(self) -> bool:
        try:
            self.serial = serial.Serial(
                self.port, self.baudrate, timeout=1
            )
            return True
        except Exception:
            return False
    
    def query(self, command: str) -> str:
        self.serial.write(command.encode() + b'\n')
        return self.serial.readline().decode().strip()
```

### GUI与仪器分离

```python
class InstrumentController(QObject):
    """仪器控制器 - 连接GUI和仪器"""
    
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    data_received = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, instrument: InstrumentBase):
        super().__init__()
        self.instrument = instrument
        self.polling_timer = QTimer()
        self.polling_timer.timeout.connect(self.poll_data)
    
    def start_polling(self, interval: int = 1000):
        """开始轮询数据"""
        self.polling_timer.start(interval)
    
    def poll_data(self):
        """轮询仪器数据"""
        try:
            data = {
                'temperature': float(self.instrument.query(':TEMP?')),
                'status': self.instrument.query(':STAT?')
            }
            self.data_received.emit(data)
        except Exception as e:
            self.error.emit(str(e))
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **温度控制器**：实时监控、PID控制、数据记录
2. **信号发生器**：波形生成、参数调节、输出控制
3. **数据采集**：多通道采集、实时显示、数据存储
4. **仪器框架**：分层设计、接口抽象、可扩展架构

### 开发最佳实践

1. **模块化设计**
   - 仪器驱动独立于GUI
   - 便于单元测试
   - 易于更换仪器

2. **错误处理**
   - 通信异常捕获
   - 重连机制
   - 用户友好提示

3. **性能优化**
   - 批量数据处理
   - 图形更新节流
   - 内存管理

4. **用户体验**
   - 直观的界面布局
   - 实时状态反馈
   - 快捷键支持

---

## 下一章预告

[第八章：项目实战与部署](../ch08_project/) - 完整项目开发、打包部署、性能优化。

