# 1.4 模板基础

## 📖 本节概述

模板是C++泛型编程的核心特性，允许我们编写与类型无关的代码。本节将回顾函数模板、类模板的基本用法，并介绍一些现代C++中的模板新特性。

---

## 1. 为什么需要模板

### 1.1 问题：代码重复

```cpp
// 没有模板时，需要为每种类型写重复代码
int max_int(int a, int b) {
    return (a > b) ? a : b;
}

double max_double(double a, double b) {
    return (a > b) ? a : b;
}

std::string max_string(const std::string& a, const std::string& b) {
    return (a > b) ? a : b;
}
```

### 1.2 解决方案：模板

```cpp
// 一个模板，适用于所有可比较的类型
template<typename T>
T max_value(T a, T b) {
    return (a > b) ? a : b;
}

// 使用
int i = max_value(3, 5);              // T = int
double d = max_value(3.14, 2.71);     // T = double
std::string s = max_value(std::string("abc"), std::string("xyz"));  // T = std::string
```

---

## 2. 函数模板

### 2.1 基本语法

```cpp
// 定义函数模板
template<typename T>  // 或 template<class T>，两者等价
T add(T a, T b) {
    return a + b;
}

// 使用
int sum1 = add<int>(1, 2);        // 显式指定类型
int sum2 = add(1, 2);             // 编译器自动推断类型
double sum3 = add(1.5, 2.5);      // T = double
```

### 2.2 多个类型参数

```cpp
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// C++14：简化写法
template<typename T, typename U>
auto add(T a, U b) {
    return a + b;  // 返回类型自动推断
}

// 使用
auto result = add(1, 2.5);  // int + double = double
```

### 2.3 非类型模板参数

```cpp
// 非类型参数：编译期常量
template<typename T, int N>
class FixedArray {
private:
    T data_[N];

public:
    int size() const { return N; }
    T& operator[](int index) { return data_[index]; }
    const T& operator[](int index) const { return data_[index]; }
};

FixedArray<int, 10> arr;  // 10个int的数组

// 函数中的非类型参数
template<int N>
int multiply(int x) {
    return x * N;
}

int result = multiply<5>(10);  // 50
```

### 2.4 默认模板参数

```cpp
template<typename T = int, typename Allocator = std::allocator<T>>
class Container {
    // ...
};

Container<> c1;                    // T = int, 默认分配器
Container<double> c2;              // T = double, 默认分配器
Container<int, MyAllocator<int>> c3;  // 自定义分配器
```

---

## 3. 类模板

### 3.1 基本类模板

```cpp
template<typename T>
class Stack {
private:
    std::vector<T> data_;

public:
    void push(const T& value) {
        data_.push_back(value);
    }
    
    void pop() {
        if (!data_.empty()) {
            data_.pop_back();
        }
    }
    
    T& top() {
        return data_.back();
    }
    
    const T& top() const {
        return data_.back();
    }
    
    bool empty() const {
        return data_.empty();
    }
    
    size_t size() const {
        return data_.size();
    }
};

// 使用
Stack<int> int_stack;
int_stack.push(1);
int_stack.push(2);
std::cout << int_stack.top() << std::endl;  // 2

Stack<std::string> string_stack;
string_stack.push("hello");
```

### 3.2 类模板成员函数定义

```cpp
// 头文件中定义（推荐）
template<typename T>
class MyClass {
public:
    void foo();
    T bar(T x);
};

// 成员函数在类外定义
template<typename T>
void MyClass<T>::foo() {
    // 实现
}

template<typename T>
T MyClass<T>::bar(T x) {
    return x;
}

// 注意：模板的实现通常放在头文件中
// 因为编译器需要在实例化时看到完整定义
```

### 3.3 类模板的静态成员

```cpp
template<typename T>
class Counter {
public:
    static int count;
    
    Counter() { ++count; }
    ~Counter() { --count; }
};

// 静态成员定义
template<typename T>
int Counter<T>::count = 0;

// 每个模板实例化都有自己的静态成员
Counter<int> a, b, c;
std::cout << Counter<int>::count << std::endl;    // 3

Counter<double> d;
std::cout << Counter<double>::count << std::endl; // 1
```

---

## 4. 模板特化

### 4.1 完全特化

```cpp
// 通用模板
template<typename T>
class Printer {
public:
    static void print(const T& value) {
        std::cout << value << std::endl;
    }
};

// 针对 bool 的完全特化
template<>
class Printer<bool> {
public:
    static void print(bool value) {
        std::cout << (value ? "true" : "false") << std::endl;
    }
};

// 针对 const char* 的完全特化
template<>
class Printer<const char*> {
public:
    static void print(const char* value) {
        std::cout << "String: " << value << std::endl;
    }
};

// 使用
Printer<int>::print(42);           // 42
Printer<bool>::print(true);        // true
Printer<const char*>::print("hi"); // String: hi
```

### 4.2 部分特化（偏特化）

```cpp
// 通用模板
template<typename T, typename U>
class Pair {
public:
    T first;
    U second;
    
    void print() {
        std::cout << "Generic: " << first << ", " << second << std::endl;
    }
};

// 两个参数相同时的部分特化
template<typename T>
class Pair<T, T> {
public:
    T first;
    T second;
    
    void print() {
        std::cout << "Same type: " << first << ", " << second << std::endl;
    }
};

// 第二个参数是 int 时的部分特化
template<typename T>
class Pair<T, int> {
public:
    T first;
    int second;
    
    void print() {
        std::cout << "Second is int: " << first << ", " << second << std::endl;
    }
};

// 指针类型的部分特化
template<typename T>
class Pair<T*, T*> {
public:
    T* first;
    T* second;
    
    void print() {
        std::cout << "Pointers: " << *first << ", " << *second << std::endl;
    }
};
```

### 4.3 函数模板特化

```cpp
// 通用模板
template<typename T>
T abs_value(T x) {
    return x < 0 ? -x : x;
}

// 完全特化（不推荐，用重载代替）
template<>
int abs_value<int>(int x) {
    return x < 0 ? -x : x;
}

// 更好的方式：使用重载
int abs_value(int x) {
    return x < 0 ? -x : x;
}

// 注意：函数模板不支持部分特化，使用重载或 SFINAE
```

---

## 5. 模板与类型推断

### 5.1 auto 与模板

```cpp
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;  // C++14：自动推断返回类型
}

// C++11：需要尾置返回类型
template<typename T, typename U>
auto multiply_cpp11(T a, U b) -> decltype(a * b) {
    return a * b;
}
```

### 5.2 decltype

```cpp
int x = 10;
decltype(x) y = 20;       // y 是 int
decltype((x)) z = x;      // z 是 int&（加括号变引用）

template<typename Container>
auto get_size(const Container& c) -> decltype(c.size()) {
    return c.size();
}
```

### 5.3 C++17 类模板参数推断（CTAD）

```cpp
// C++17 之前：必须指定模板参数
std::vector<int> v1 = {1, 2, 3};
std::pair<int, double> p1 = {1, 3.14};

// C++17：可以自动推断
std::vector v2 = {1, 2, 3};           // vector<int>
std::pair p2 = {1, 3.14};             // pair<int, double>

// 自定义类也可以使用 CTAD
template<typename T>
class Wrapper {
public:
    T value;
    Wrapper(T v) : value(v) {}
};

Wrapper w = 42;  // Wrapper<int>

// 推断指南（Deduction Guide）
template<typename T>
Wrapper(T) -> Wrapper<T>;
```

---

## 6. 可变参数模板（C++11）

### 6.1 基本语法

```cpp
// 可变参数模板
template<typename... Args>
void print(Args... args) {
    // sizeof... 获取参数个数
    std::cout << "Number of arguments: " << sizeof...(args) << std::endl;
}

print(1, 2, 3);              // 3
print("hello", 42, 3.14);    // 3
print();                     // 0
```

### 6.2 递归展开

```cpp
// 基础情况：无参数
void print() {
    std::cout << std::endl;
}

// 递归情况：至少一个参数
template<typename T, typename... Args>
void print(T first, Args... rest) {
    std::cout << first << " ";
    print(rest...);  // 递归调用
}

print(1, 2.5, "hello", 'c');  // 1 2.5 hello c
```

### 6.3 C++17 折叠表达式

```cpp
// C++17：折叠表达式，更简洁
template<typename... Args>
auto sum(Args... args) {
    return (... + args);  // 一元左折叠
    // 等价于 ((arg1 + arg2) + arg3) + ...
}

template<typename... Args>
void print_all(Args... args) {
    ((std::cout << args << " "), ...);  // 逗号表达式折叠
    std::cout << std::endl;
}

int total = sum(1, 2, 3, 4, 5);  // 15
print_all(1, "hello", 3.14);     // 1 hello 3.14
```

### 6.4 折叠表达式的类型

```cpp
// (... op args)     一元左折叠  ((a1 op a2) op a3) op ...
// (args op ...)     一元右折叠  a1 op (a2 op (a3 op ...))
// (init op ... op args)  二元左折叠
// (args op ... op init)  二元右折叠

template<typename... Args>
bool all_true(Args... args) {
    return (... && args);  // 所有参数都为true
}

template<typename... Args>
bool any_true(Args... args) {
    return (... || args);  // 任一参数为true
}
```

---

## 7. SFINAE 与 Concepts

### 7.1 SFINAE（替换失败不是错误）

```cpp
#include <type_traits>

// 使用 SFINAE 限制模板
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
double_value(T x) {
    return x * 2;
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
double_value(T x) {
    return x * 2.0;
}

// C++14 简化
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
triple_value(T x) {
    return x * 3;
}
```

### 7.2 C++20 Concepts

```cpp
#include <concepts>

// 定义概念
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::convertible_to<T>;
};

// 使用概念约束模板
template<Numeric T>
T add(T a, T b) {
    return a + b;
}

// 或者使用 requires 子句
template<typename T>
    requires Addable<T>
T add2(T a, T b) {
    return a + b;
}

// 更简洁的语法
auto add3(Numeric auto a, Numeric auto b) {
    return a + b;
}
```

### 7.3 标准库 Concepts（C++20）

```cpp
#include <concepts>

// 常用标准概念
template<std::integral T>
T gcd(T a, T b) {
    while (b != 0) {
        T t = b;
        b = a % b;
        a = t;
    }
    return a;
}

template<std::floating_point T>
T average(T a, T b) {
    return (a + b) / 2.0;
}

// std::same_as, std::derived_from, std::convertible_to
// std::integral, std::floating_point, std::signed_integral
// std::default_initializable, std::copyable, std::movable
// 等等...
```

---

## 8. 模板最佳实践

### 8.1 模板代码组织

```cpp
// Option 1：全部放在头文件（最常用）
// my_template.hpp
template<typename T>
class MyTemplate {
public:
    void foo() {
        // 实现
    }
};

// Option 2：声明和定义分离，但都在头文件
// my_template.hpp
template<typename T>
class MyTemplate {
public:
    void foo();
};

// 在同一头文件的底部
template<typename T>
void MyTemplate<T>::foo() {
    // 实现
}

// Option 3：显式实例化（减少编译时间）
// my_template.hpp（声明）
template<typename T>
class MyTemplate {
public:
    void foo();
};

// my_template.cpp（定义 + 显式实例化）
template<typename T>
void MyTemplate<T>::foo() {
    // 实现
}

// 显式实例化常用类型
template class MyTemplate<int>;
template class MyTemplate<double>;
template class MyTemplate<std::string>;
```

### 8.2 避免模板膨胀

```cpp
// 问题：每种类型都生成一份代码
template<typename T>
void process(T* data, size_t size) {
    // 大量代码...
}

// 解决方案：提取与类型无关的代码
void process_impl(void* data, size_t size, size_t element_size);

template<typename T>
void process(T* data, size_t size) {
    process_impl(data, size, sizeof(T));
}
```

---

## 📝 练习题

### 练习1：泛型 swap
实现一个泛型 `swap` 函数模板，交换两个同类型的值。

### 练习2：简单 Vector
实现一个简单的 `Vector` 类模板，支持 `push_back`、`size`、`operator[]`。

### 练习3：类型萃取
使用 `std::is_integral` 和 SFINAE（或 Concepts）实现一个函数，对整数返回绝对值，对浮点数返回平方根。

### 练习4：可变参数 max
实现一个可变参数模板函数 `max_of`，返回所有参数中的最大值。

---

## 💡 要点总结

1. **模板是编译期特性**：代码在编译时根据使用的类型生成
2. **优先使用 auto**：简化模板代码
3. **模板实现放在头文件**：编译器需要看到完整定义
4. **使用 Concepts（C++20）**：比 SFINAE 更清晰
5. **注意模板膨胀**：相同逻辑的不同类型实例化会增加代码大小
6. **函数模板用重载而非特化**：避免特化的陷阱

---

## ⏭️ 下一节

[1.5 STL容器](./05_stl_containers.md) - 掌握标准库的数据结构

