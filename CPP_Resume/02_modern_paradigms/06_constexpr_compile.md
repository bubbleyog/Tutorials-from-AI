# 2.6 编译期计算

## 📖 本节概述

编译期计算是现代 C++ 的强大特性，它让我们可以在编译时执行计算，从而提升运行时性能并启用一些特殊的编程技巧。本节将深入讲解 `constexpr`、`if constexpr` 以及 C++20 的增强特性。

---

## 1. const vs constexpr

### 1.1 const 的含义

```cpp
const int x = 10;        // 编译期常量
const int y = get_value(); // 运行时常量

// const 表示"不可修改"，但不保证在编译期可用
const int size = 100;
int arr[size];           // ✅ OK，size 是编译期常量

const int runtime = get_value();
// int arr2[runtime];    // ❌ 可能失败，取决于编译器
```

### 1.2 constexpr 的含义

```cpp
constexpr int x = 10;           // 必须是编译期常量
// constexpr int y = get_value(); // ❌ 编译错误

// constexpr 保证在编译期可用
constexpr int size = 100;
int arr[size];                   // ✅ 一定可以

// constexpr 隐含 const
constexpr int z = 42;
// z = 100;  // ❌ 错误，z 是 const
```

### 1.3 对比

| 特性 | const | constexpr |
|------|-------|-----------|
| 编译期确定 | 可能 | 必须 |
| 可用作数组大小 | 有时 | 总是 |
| 可用于模板参数 | 有时 | 总是 |
| 可在运行时初始化 | 可以 | 不可以 |

---

## 2. constexpr 函数

### 2.1 C++11 constexpr 函数

```cpp
// C++11：非常严格，只能有一个 return 语句
constexpr int factorial_11(int n) {
    return n <= 1 ? 1 : n * factorial_11(n - 1);
}

// 可以在编译期使用
constexpr int fact5 = factorial_11(5);  // 120，编译期计算
static_assert(factorial_11(5) == 120, "Wrong!");

// 也可以在运行时使用
int n = get_value();
int result = factorial_11(n);  // 运行时计算
```

### 2.2 C++14 constexpr 函数

```cpp
// C++14：放宽限制，可以有多条语句
constexpr int factorial_14(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// 可以有局部变量、循环、条件语句
constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    
    int a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

constexpr int fib10 = fibonacci(10);  // 55
```

### 2.3 C++20 constexpr 函数

```cpp
// C++20：更多能力
#include <vector>
#include <string>
#include <algorithm>

// constexpr 虚函数
class Base {
public:
    constexpr virtual int get_value() const { return 0; }
};

class Derived : public Base {
public:
    constexpr int get_value() const override { return 42; }
};

// constexpr 动态分配（编译期临时）
constexpr int sum_vector() {
    std::vector<int> v = {1, 2, 3, 4, 5};  // C++20
    int sum = 0;
    for (int x : v) sum += x;
    return sum;
}

constexpr int result = sum_vector();  // 15

// constexpr std::string（C++20）
constexpr std::string make_greeting() {
    std::string s = "Hello, ";
    s += "World!";
    return s;
}
```

### 2.4 constexpr 函数的规则

```cpp
// 允许的（各版本逐渐放宽）
constexpr int allowed() {
    int x = 10;          // C++14+：局部变量
    x += 5;              // C++14+：修改
    if (x > 10) x = 10;  // C++14+：条件
    for (int i = 0; i < 5; ++i) x += i;  // C++14+：循环
    return x;
}

// 不允许的
constexpr int not_allowed() {
    // static int x = 0;        // ❌ 静态变量
    // thread_local int y = 0;  // ❌ 线程局部
    // std::cout << "hi";       // ❌ I/O
    // throw std::exception();  // ❌ C++20 之前不允许 try-catch
    return 0;
}
```

---

## 3. constexpr 变量

### 3.1 基本用法

```cpp
constexpr int max_size = 100;
constexpr double pi = 3.14159265358979;

// 用于数组大小
int arr[max_size];

// 用于模板参数
std::array<int, max_size> std_arr;

// 表达式
constexpr int doubled = max_size * 2;
```

### 3.2 constexpr 与类

```cpp
class Point {
public:
    int x, y;
    
    // constexpr 构造函数
    constexpr Point(int x, int y) : x(x), y(y) {}
    
    // constexpr 成员函数
    constexpr int manhattan_distance() const {
        return (x >= 0 ? x : -x) + (y >= 0 ? y : -y);
    }
    
    constexpr Point operator+(const Point& other) const {
        return Point(x + other.x, y + other.y);
    }
};

// 编译期创建和使用
constexpr Point p1(3, 4);
constexpr Point p2(1, 2);
constexpr Point p3 = p1 + p2;  // (4, 6)
constexpr int dist = p1.manhattan_distance();  // 7

static_assert(p3.x == 4 && p3.y == 6, "Wrong!");
```

---

## 4. if constexpr (C++17)

### 4.1 编译期条件分支

```cpp
#include <type_traits>

template<typename T>
auto process(T value) {
    if constexpr (std::is_integral_v<T>) {
        // 整数：返回平方
        return value * value;
    } else if constexpr (std::is_floating_point_v<T>) {
        // 浮点：返回一半
        return value / 2.0;
    } else {
        // 其他：返回原值
        return value;
    }
}

int main() {
    auto a = process(5);      // 25
    auto b = process(3.14);   // 1.57
    auto c = process(std::string("hi"));  // "hi"
}
```

### 4.2 if constexpr vs 普通 if

```cpp
template<typename T>
void print_type(T value) {
    // 普通 if：两个分支都必须能编译
    if (std::is_integral_v<T>) {
        std::cout << value % 2 << std::endl;  // ❌ 对浮点类型编译错误
    }
    
    // if constexpr：未选中的分支不需要能编译
    if constexpr (std::is_integral_v<T>) {
        std::cout << value % 2 << std::endl;  // ✅ 只在 T 是整数时编译
    } else {
        std::cout << value / 2.0 << std::endl;
    }
}
```

### 4.3 替代 SFINAE

```cpp
// C++14 之前：SFINAE
template<typename T>
typename std::enable_if<std::is_integral_v<T>, T>::type
double_value(T x) { return x * 2; }

template<typename T>
typename std::enable_if<std::is_floating_point_v<T>, T>::type
double_value(T x) { return x * 2.0; }

// C++17：if constexpr（更清晰）
template<typename T>
auto double_value(T x) {
    if constexpr (std::is_integral_v<T>) {
        return x * 2;
    } else {
        return x * 2.0;
    }
}
```

### 4.4 递归模板终止

```cpp
// 使用 if constexpr 终止递归
template<typename T, typename... Ts>
void print_all(T first, Ts... rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) {
        std::cout << ", ";
        print_all(rest...);
    } else {
        std::cout << std::endl;
    }
}

// 使用
print_all(1, 2.5, "hello", 'c');  // 1, 2.5, hello, c
```

---

## 5. consteval 和 constinit (C++20)

### 5.1 consteval：强制编译期执行

```cpp
// consteval：必须在编译期执行
consteval int square(int n) {
    return n * n;
}

constexpr int a = square(5);  // ✅ OK，编译期

int x = 5;
// int b = square(x);  // ❌ 错误：x 不是编译期常量

// 对比 constexpr
constexpr int cube(int n) {
    return n * n * n;
}

int c = cube(x);  // ✅ OK，运行时调用
```

### 5.2 constinit：强制编译期初始化

```cpp
// constinit：变量必须在编译期初始化，但运行时可修改
constinit int global = 42;  // 编译期初始化

void modify() {
    global = 100;  // ✅ 可以修改
}

// 用途：避免静态初始化顺序问题
// constinit 保证在程序启动时就已初始化

// 对比
constexpr int constant = 42;  // 编译期常量，不能修改
// constant = 100;  // ❌ 错误
```

### 5.3 对比三者

| 关键字 | 编译期初始化 | 编译期可用 | 运行时可修改 | 运行时可调用 |
|--------|-------------|-----------|-------------|-------------|
| `const` | 可能 | 可能 | ❌ | - |
| `constexpr` | ✅ 必须 | ✅ | ❌ | ✅ 可以 |
| `consteval` | ✅ 必须 | ✅ | - | ❌ 必须编译期 |
| `constinit` | ✅ 必须 | ✅ | ✅ | - |

---

## 6. 编译期编程技巧

### 6.1 编译期字符串处理

```cpp
// C++17：编译期字符串
constexpr size_t string_length(const char* s) {
    size_t len = 0;
    while (s[len] != '\0') ++len;
    return len;
}

constexpr auto len = string_length("Hello");  // 5
static_assert(len == 5);

// C++20：编译期 std::string
constexpr std::string concat() {
    std::string a = "Hello, ";
    std::string b = "World!";
    return a + b;
}
```

### 6.2 编译期数组操作

```cpp
#include <array>

constexpr std::array<int, 5> create_array() {
    std::array<int, 5> arr{};
    for (int i = 0; i < 5; ++i) {
        arr[i] = i * i;
    }
    return arr;
}

constexpr auto squares = create_array();  // {0, 1, 4, 9, 16}
static_assert(squares[2] == 4);

// 编译期排序
constexpr std::array<int, 5> sort_array(std::array<int, 5> arr) {
    // 简单冒泡排序
    for (size_t i = 0; i < arr.size(); ++i) {
        for (size_t j = i + 1; j < arr.size(); ++j) {
            if (arr[i] > arr[j]) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
    return arr;
}

constexpr std::array<int, 5> unsorted = {5, 2, 4, 1, 3};
constexpr auto sorted = sort_array(unsorted);  // {1, 2, 3, 4, 5}
```

### 6.3 编译期查找表

```cpp
// 编译期生成查找表
constexpr std::array<int, 256> create_lookup_table() {
    std::array<int, 256> table{};
    for (int i = 0; i < 256; ++i) {
        // 某种转换逻辑
        table[i] = (i * 17) % 256;
    }
    return table;
}

constexpr auto lookup = create_lookup_table();

// 运行时快速查找
int fast_transform(unsigned char c) {
    return lookup[c];  // 零计算开销
}
```

### 6.4 类型特征

```cpp
#include <type_traits>

// 自定义类型特征
template<typename T>
constexpr bool is_string_like = 
    std::is_same_v<T, std::string> ||
    std::is_same_v<T, std::string_view> ||
    std::is_same_v<T, const char*>;

// 使用
static_assert(is_string_like<std::string>);
static_assert(is_string_like<const char*>);
static_assert(!is_string_like<int>);
```

---

## 7. static_assert

### 7.1 编译期断言

```cpp
// 基本用法
static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");

// C++17：消息可选
static_assert(sizeof(int) >= 4);

// 模板中使用
template<typename T>
class OnlyForIntegral {
    static_assert(std::is_integral_v<T>, "T must be integral");
public:
    T value;
};

OnlyForIntegral<int> ok;
// OnlyForIntegral<double> fail;  // 编译错误
```

### 7.2 配合 constexpr 使用

```cpp
constexpr bool is_power_of_two(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

static_assert(is_power_of_two(1));
static_assert(is_power_of_two(2));
static_assert(is_power_of_two(16));
static_assert(!is_power_of_two(15));

template<int N>
class AlignedBuffer {
    static_assert(is_power_of_two(N), "N must be power of 2");
    alignas(N) char buffer[N];
};

AlignedBuffer<16> good;
// AlignedBuffer<15> bad;  // 编译错误
```

---

## 8. 最佳实践

### 8.1 何时使用 constexpr

```cpp
// ✅ 使用 constexpr
// 1. 编译期常量
constexpr double PI = 3.14159265358979;
constexpr int MAX_SIZE = 1024;

// 2. 可以在编译期计算的简单函数
constexpr int square(int n) { return n * n; }

// 3. 需要用于模板参数或数组大小的值
constexpr int N = 10;
std::array<int, N> arr;

// 4. 性能关键的查找表
constexpr auto table = generate_table();
```

### 8.2 constexpr 函数设计

```cpp
// 好的 constexpr 函数设计
// 1. 纯函数（无副作用）
constexpr int add(int a, int b) { return a + b; }

// 2. 可以在运行时和编译期使用
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

// 编译期
constexpr int f5 = factorial(5);

// 运行时
int n = get_input();
int fn = factorial(n);
```

### 8.3 调试 constexpr

```cpp
// 使用 static_assert 验证
constexpr int result = some_constexpr_function();
static_assert(result == expected, "Unexpected result!");

// 编译期打印（C++20 consteval + C++23）
// 暂时不支持直接打印

// 拆分成小函数，逐步验证
constexpr int step1 = process_step1(input);
static_assert(step1 == 10);

constexpr int step2 = process_step2(step1);
static_assert(step2 == 20);
```

---

## 📝 练习题

### 练习1：编译期斐波那契
实现 constexpr 斐波那契函数，使用 static_assert 验证结果。

### 练习2：编译期字符串哈希
实现一个 constexpr 字符串哈希函数，可用于编译期 switch 字符串。

### 练习3：if constexpr 类型处理
使用 if constexpr 实现一个函数，对不同类型的容器执行不同操作。

### 练习4：编译期素数检测
实现 constexpr 素数检测函数，生成一个编译期素数表。

---

## 💡 要点总结

1. **constexpr**：值/函数必须能在编译期计算
2. **consteval**（C++20）：函数必须在编译期执行
3. **constinit**（C++20）：变量必须在编译期初始化
4. **if constexpr**（C++17）：编译期条件分支，未选分支不编译
5. **static_assert**：编译期断言，验证条件
6. **C++20 大幅增强 constexpr**：支持 vector、string、动态分配
7. **编译期计算提升运行时性能**：预计算查找表等

---

## ⏭️ 下一节

[2.7 现代错误处理](./07_error_handling.md) - 探索异常、optional 和 expected

