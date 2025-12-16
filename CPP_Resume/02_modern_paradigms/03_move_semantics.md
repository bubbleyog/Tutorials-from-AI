# 2.3 移动语义与完美转发

## 📖 本节概述

移动语义是 C++11 引入的最重要特性之一。它允许我们**转移资源的所有权**而不是拷贝，从而极大地提升了性能。理解移动语义需要先理解**值类别**（左值和右值）的概念。

本节是现代 C++ 中最具挑战性但也最重要的内容之一。

---

## 1. 值类别：左值与右值

### 1.1 基本概念

简单来说：
- **左值（lvalue）**：有名字、有地址、可以取地址的表达式
- **右值（rvalue）**：临时的、即将销毁的、不能取地址的表达式

```cpp
int x = 10;     // x 是左值
int y = x + 5;  // x + 5 是右值

// 可以取地址 → 左值
int* p = &x;    // ✅

// 不能取地址 → 右值
// int* p2 = &(x + 5);  // ❌ 编译错误
// int* p3 = &10;       // ❌ 编译错误
```

### 1.2 更多例子

```cpp
int x = 10;
int& ref = x;

// 左值
x               // 变量
ref             // 引用
*p              // 解引用
arr[0]          // 下标访问
++x             // 前置自增（返回引用）
"hello"         // 字符串字面量（特殊，是左值）

// 右值
42              // 字面量
x + y           // 算术表达式
x++             // 后置自增（返回旧值的拷贝）
make_pair(1,2)  // 临时对象
std::move(x)    // std::move 的结果
```

### 1.3 C++11 的值类别细分

C++11 将值类别进一步细分：

```
           表达式
          /      \
       glvalue   rvalue
       /    \    /    \
    lvalue  xvalue   prvalue
```

- **lvalue**：传统左值
- **prvalue**：纯右值（字面量、临时对象）
- **xvalue**：将亡值（`std::move` 的结果）
- **glvalue**：广义左值（lvalue + xvalue）
- **rvalue**：右值（xvalue + prvalue）

对于日常使用，理解左值和右值就够了。

---

## 2. 右值引用

### 2.1 左值引用 vs 右值引用

```cpp
int x = 10;

// 左值引用：只能绑定到左值
int& lref = x;        // ✅
// int& lref2 = 10;   // ❌ 不能绑定到右值

// const 左值引用：可以绑定到右值（特殊规则）
const int& clref = 10;  // ✅ 延长临时对象生命周期

// 右值引用：只能绑定到右值
int&& rref = 10;       // ✅
int&& rref2 = x + 5;   // ✅
// int&& rref3 = x;    // ❌ 不能绑定到左值
```

### 2.2 右值引用的用途

右值引用的主要用途是**识别临时对象**，从而可以安全地"窃取"其资源：

```cpp
void process(int& x) {
    std::cout << "lvalue: " << x << std::endl;
}

void process(int&& x) {
    std::cout << "rvalue: " << x << std::endl;
}

int main() {
    int a = 10;
    process(a);      // 调用 process(int&)
    process(20);     // 调用 process(int&&)
    process(a + 5);  // 调用 process(int&&)
}
```

---

## 3. 移动语义

### 3.1 为什么需要移动

考虑这个场景：

```cpp
std::vector<int> create_vector() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    return v;  // 返回时会发生什么？
}

int main() {
    std::vector<int> result = create_vector();
}
```

在 C++11 之前，返回 `v` 会触发拷贝构造——复制整个数组。
在 C++11 之后，编译器识别出 `v` 即将被销毁，可以**移动**而非拷贝。

### 3.2 移动构造函数和移动赋值运算符

```cpp
class Buffer {
private:
    int* data_;
    size_t size_;

public:
    // 构造函数
    Buffer(size_t size) : data_(new int[size]), size_(size) {
        std::cout << "Constructor: allocate " << size << std::endl;
    }
    
    // 析构函数
    ~Buffer() {
        delete[] data_;
        std::cout << "Destructor" << std::endl;
    }
    
    // 拷贝构造函数
    Buffer(const Buffer& other) 
        : data_(new int[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
        std::cout << "Copy constructor" << std::endl;
    }
    
    // 拷贝赋值运算符
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new int[size_];
            std::copy(other.data_, other.data_ + size_, data_);
        }
        std::cout << "Copy assignment" << std::endl;
        return *this;
    }
    
    // 移动构造函数 ✨
    Buffer(Buffer&& other) noexcept
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;  // 重要：置空源对象
        other.size_ = 0;
        std::cout << "Move constructor" << std::endl;
    }
    
    // 移动赋值运算符 ✨
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;       // 释放自己的资源
            data_ = other.data_;  // 接管源对象的资源
            size_ = other.size_;
            other.data_ = nullptr; // 置空源对象
            other.size_ = 0;
        }
        std::cout << "Move assignment" << std::endl;
        return *this;
    }
};
```

### 3.3 移动 vs 拷贝的性能差异

```cpp
void demo_performance() {
    Buffer b1(1000000);  // 分配 1MB
    
    Buffer b2 = b1;      // 拷贝：分配新内存，复制数据
    // 时间复杂度：O(n)
    
    Buffer b3 = std::move(b1);  // 移动：只是转移指针
    // 时间复杂度：O(1)
    
    // b1 现在处于有效但未指定的状态
    // 通常资源已被转移，但对象仍然可以安全销毁
}
```

---

## 4. std::move

### 4.1 std::move 的本质

`std::move` **不移动任何东西**！它只是将左值转换为右值引用：

```cpp
template<typename T>
typename std::remove_reference<T>::type&& move(T&& t) noexcept {
    return static_cast<typename std::remove_reference<T>::type&&>(t);
}
```

简化理解：`std::move(x)` 就是 `static_cast<X&&>(x)`

### 4.2 使用 std::move

```cpp
#include <utility>

void demo_std_move() {
    std::string s1 = "Hello";
    
    // std::move 只是类型转换，不会立即移动
    std::string&& rref = std::move(s1);
    // s1 仍然有效
    
    // 真正的移动发生在这里（调用移动构造函数）
    std::string s2 = std::move(s1);
    // s1 现在为空（资源被转移）
    
    std::cout << "s1: '" << s1 << "'" << std::endl;  // 可能为空
    std::cout << "s2: '" << s2 << "'" << std::endl;  // "Hello"
}
```

### 4.3 何时使用 std::move

```cpp
// 1. 转移所有权
void take_ownership(std::unique_ptr<Widget> w);
auto w = std::make_unique<Widget>();
take_ownership(std::move(w));  // 必须移动，unique_ptr 不能拷贝

// 2. 最后一次使用某个对象
std::vector<std::string> collect_strings() {
    std::vector<std::string> result;
    std::string temp;
    
    while (read_next(temp)) {
        result.push_back(std::move(temp));  // 移动而非拷贝
        temp.clear();  // 可选：重新使用 temp
    }
    
    return result;  // 自动移动（NRVO 或移动）
}

// 3. swap 的实现
template<typename T>
void my_swap(T& a, T& b) {
    T temp = std::move(a);
    a = std::move(b);
    b = std::move(temp);
}
```

### 4.4 不要过度使用 std::move

```cpp
// ❌ 不要移动返回的局部变量（阻止 RVO）
std::vector<int> bad() {
    std::vector<int> v = {1, 2, 3};
    return std::move(v);  // 反而可能更慢！
}

// ✅ 直接返回，让编译器优化
std::vector<int> good() {
    std::vector<int> v = {1, 2, 3};
    return v;  // 编译器会自动优化（RVO 或隐式移动）
}

// ❌ 不要移动 const 对象（会变成拷贝）
const std::string s = "Hello";
std::string s2 = std::move(s);  // 实际是拷贝！
```

---

## 5. 完美转发

### 5.1 问题：如何保持参数的值类别？

```cpp
template<typename T>
void wrapper(T arg) {
    target(arg);  // arg 是左值！即使传入的是右值
}

wrapper(42);  // 42 是右值，但 arg 是左值
```

### 5.2 转发引用（通用引用）

当 `T&&` 与模板类型推断结合时，它变成**转发引用**：

```cpp
template<typename T>
void wrapper(T&& arg) {  // 转发引用，不是右值引用！
    // T&& 可以绑定到左值或右值
}

int x = 10;
wrapper(x);   // T = int&, arg 类型为 int& （引用折叠）
wrapper(10);  // T = int,  arg 类型为 int&&
```

### 5.3 引用折叠规则

```cpp
// 引用的引用会折叠
T& &   → T&
T& &&  → T&
T&& &  → T&
T&& && → T&&

// 规则：只要有左值引用，结果就是左值引用
```

### 5.4 std::forward

`std::forward` 保持参数的原始值类别：

```cpp
#include <utility>

template<typename T>
void wrapper(T&& arg) {
    target(std::forward<T>(arg));  // 完美转发
}

void target(int& x)  { std::cout << "lvalue" << std::endl; }
void target(int&& x) { std::cout << "rvalue" << std::endl; }

int main() {
    int x = 10;
    wrapper(x);   // 输出 "lvalue"
    wrapper(10);  // 输出 "rvalue"
}
```

### 5.5 完美转发的实际应用

```cpp
// make_unique 的简化实现
template<typename T, typename... Args>
std::unique_ptr<T> my_make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// emplace_back 的原理
template<typename T>
class MyVector {
    // ...
public:
    template<typename... Args>
    void emplace_back(Args&&... args) {
        // 在容器内部原地构造对象
        new (end_ptr) T(std::forward<Args>(args)...);
    }
};
```

### 5.6 转发引用 vs 右值引用

```cpp
// 这是右值引用
void foo(int&& x);           // 明确的类型，是右值引用

// 这是转发引用
template<typename T>
void bar(T&& x);             // 模板参数 + &&，是转发引用

// auto&& 也是转发引用
auto&& x = expr;

// 以下是右值引用，不是转发引用
template<typename T>
void baz(std::vector<T>&& v);  // 不是简单的 T&&，是右值引用

template<typename T>
class Wrapper {
    void qux(T&& x);  // T 不在此函数推断，是右值引用
};
```

---

## 6. 移动语义的最佳实践

### 6.1 实现移动操作的规则

```cpp
class Resource {
public:
    // 1. 移动构造函数应该是 noexcept
    Resource(Resource&& other) noexcept;
    
    // 2. 移动赋值运算符应该是 noexcept
    Resource& operator=(Resource&& other) noexcept;
    
    // 3. 移动后的源对象应该处于有效但未指定的状态
    // 4. 析构函数应该能正确处理移动后的对象
};
```

### 6.2 为什么 noexcept 很重要

```cpp
// std::vector 在重新分配时的行为
std::vector<MyClass> v;
v.reserve(10);
// 添加元素...
v.reserve(20);  // 需要移动元素到新内存

// 如果移动构造函数是 noexcept：
// vector 使用移动 → 高效

// 如果移动构造函数可能抛出异常：
// vector 退回使用拷贝 → 保证强异常安全，但慢
```

### 6.3 五法则（Rule of Five）

如果你定义了以下任何一个，考虑定义全部五个：

```cpp
class Resource {
public:
    ~Resource();                              // 析构函数
    Resource(const Resource&);                // 拷贝构造
    Resource& operator=(const Resource&);     // 拷贝赋值
    Resource(Resource&&) noexcept;            // 移动构造
    Resource& operator=(Resource&&) noexcept; // 移动赋值
};

// 或者使用 = default / = delete 明确意图
class ModernResource {
public:
    ModernResource() = default;
    ~ModernResource() = default;
    
    ModernResource(const ModernResource&) = default;
    ModernResource& operator=(const ModernResource&) = default;
    
    ModernResource(ModernResource&&) noexcept = default;
    ModernResource& operator=(ModernResource&&) noexcept = default;
};
```

### 6.4 零法则（Rule of Zero）

最好的选择是：让编译器为你生成所有特殊成员函数：

```cpp
class Widget {
private:
    std::string name_;                    // 自带移动语义
    std::vector<int> data_;               // 自带移动语义
    std::unique_ptr<Resource> resource_;  // 自带移动语义
    
public:
    // 不需要定义任何特殊成员函数！
    // 编译器会自动生成正确的版本
};
```

---

## 7. 常见陷阱

### 7.1 移动后使用

```cpp
std::string s = "Hello";
std::string s2 = std::move(s);

// ❌ 危险：s 的状态是未指定的
std::cout << s.size() << std::endl;  // 可能是 0，可能是其他

// ✅ 安全：可以重新赋值
s = "World";
std::cout << s << std::endl;  // "World"

// ✅ 安全：可以销毁
// s 离开作用域时正常析构
```

### 7.2 const 对象不能移动

```cpp
const std::vector<int> v = {1, 2, 3};
std::vector<int> v2 = std::move(v);  // 实际是拷贝！

// 因为 std::move(v) 返回 const std::vector<int>&&
// 移动构造函数接受 std::vector<int>&&
// 所以会匹配到拷贝构造函数
```

### 7.3 移动只是优化，不是保证

```cpp
// 标准库保证移动后的对象处于有效但未指定的状态
std::string s1 = "Hello";
std::string s2 = std::move(s1);

// 不能假设 s1 一定为空！
// 只能保证 s1 可以安全销毁和重新赋值
```

---

## 📝 练习题

### 练习1：实现可移动的 String 类
创建一个简化版 String 类，实现移动构造函数和移动赋值运算符。

### 练习2：实现 make_unique
自己实现 `make_unique`，使用完美转发传递参数。

### 练习3：分析值类别
给定以下表达式，判断它们是左值还是右值：
```cpp
int x = 10;
int& r = x;
int* p = &x;

x           // ?
r           // ?
*p          // ?
x + 1       // ?
++x         // ?
x++         // ?
std::move(x) // ?
```

### 练习4：性能对比
编写测试程序，比较移动和拷贝大型容器的性能差异。

---

## 💡 要点总结

1. **左值有名字、有地址；右值是临时的**
2. **右值引用（`T&&`）用于绑定右值**，标识可以移动的对象
3. **`std::move` 只是类型转换**，不执行移动操作
4. **移动语义是窃取资源**，O(1) 代替 O(n) 的拷贝
5. **移动后对象处于有效但未指定状态**，可以销毁或重新赋值
6. **移动操作应该是 noexcept**
7. **完美转发用 `std::forward`**，保持参数的原始值类别
8. **遵循零法则**：让成员管理资源，自动获得正确的移动语义

---

## ⏭️ 下一节

[2.4 Lambda与函数式编程](./04_lambda_functional.md) - 探索 C++ 的函数式编程能力

