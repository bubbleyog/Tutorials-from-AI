# 第二章：数值计算基础与库的使用

在高性能计算中，**正确性**永远优先于**性能**。数值计算的陷阱（如浮点数精度丢失）往往比逻辑错误更难发现。同时，重复造轮子（自己写矩阵乘法或求解器）通常既慢又容易出错。

本章将介绍两个核心主题：
1.  **浮点数陷阱**：如何避免常见的数值计算错误。
2.  **Eigen 库实战**：如何使用现代 C++ 线性代数库进行高效计算。

## 1. 浮点数陷阱 (IEEE 754)

计算机使用 IEEE 754 标准表示浮点数。`float` (32位) 通常只有 7 位有效数字，`double` (64位) 有 15-16 位有效数字。

### 常见问题 1：大数吃小数 (Swallowing)
当一个非常大的数加上一个非常小的数时，由于尾数位数有限，小的数可能会被完全“吃掉”或者精度大幅损失。

**示例**：计算 $\sum_{i=1}^{10^7} 10^{-7}$，理论结果应为 1.0。
- 使用 `float` 直接累加，误差巨大。
- **解决方案**：使用 `double` 进行中间累加，或者使用 **Kahan Summation Algorithm** (补偿求和)。

> **注意**：Kahan 求和算法依赖于浮点数运算的结合律不成立这一特性（(a+b)+c != a+(b+c)）。如果你在编译时开启了 `-ffast-math` 选项，编译器可能会重新排列计算顺序，导致 Kahan 求和失效。因此，在进行高精度数值算法时，需谨慎使用全局 `-ffast-math`。

### 常见问题 2：灾难性抵消 (Catastrophic Cancellation)
当两个非常接近的数相减时，有效数字会大幅减少，导致结果主要由误差构成。

**示例**：计算 $\sqrt{x+1} - \sqrt{x}$ 当 $x$ 很大时。
- 直接相减会丢失精度。
- **解决方案**：代数变换 $\frac{1}{\sqrt{x+1} + \sqrt{x}}$。

请运行 [code/float_precision.cpp](./code/float_precision.cpp) 查看实际演示。

## 2. 线性代数库 Eigen

在 C++ HPC 开发中，**绝对不要自己编写线性代数底层算法**（如矩阵乘法、求逆、分解），除非你是为了学习算法本身。

**Eigen** 是一个高层级的 C++ 模板库，用于线性代数、矩阵和向量运算。
- **Header-only**：无需编译库文件，直接 include 即可使用。
- **Expression Templates**：惰性求值，自动消除临时变量，性能极高。
- **Vectorization**：自动使用 SSE/AVX 指令集加速。

### 核心用法

#### 定义矩阵与向量
```cpp
#include <Eigen/Dense>
Eigen::Matrix3d A; // 3x3 double 矩阵
Eigen::Vector3d v; // 3x1 double 向量
Eigen::MatrixXd M(100, 100); // 动态大小矩阵
```

#### 求解线性方程组 $Ax = b$
这是科学计算中最常见的任务。Eigen 提供了多种分解方法：

| 分解方法 | 适用矩阵 | 速度 | 精度 |
| :--- | :--- | :--- | :--- |
| **LLT (Cholesky)** | 正定矩阵 (Symmetric Positive Definite) | Very Fast | Good |
| **LDLT** | 半正定矩阵 | Fast | Good |
| **HouseholderQR** | 任意矩阵 | Medium | Good |
| **PartialPivLU** | 可逆矩阵 | Medium | Good |
| **JacobiSVD** | 任意矩阵 (求最小二乘解) | Slow | Best |

```cpp
// 推荐用法
Eigen::VectorXd x = A.llt().solve(b); // 如果已知 A 是正定的
Eigen::VectorXd x = A.colPivHouseholderQr().solve(b); // 通用解法
```

请查看 [code/eigen_example.cpp](./code/eigen_example.cpp) 了解完整代码。

## 3. 编译与运行

本章示例使用了 `FetchContent` 自动下载 Eigen 库，因此首次 CMake 配置可能需要一些时间。

```bash
cd code
mkdir build && cd build
cmake ..
make
./float_precision
./eigen_example
```

## 4. 总结

- 涉及累加时，优先使用 `double` 甚至 `long double`，或使用 Kahan 求和。
- 避免两个相近的大数相减。
- 能够使用库（Eigen, BLAS, LAPACK）解决的问题，不要手写。Eigen 是 C++ 项目的最佳起点。

---
[上一章：现代 C++ 高性能计算基础](../01_Modern_CPP_Base) | [下一章：性能分析与单核优化](../03_Performance_Optimization) (待更新)
