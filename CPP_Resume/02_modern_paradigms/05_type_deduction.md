# 2.5 类型推断

## 📖 本节概述

类型推断是现代 C++ 的重要特性，让编译器自动推断变量和表达式的类型。这不仅减少了代码冗余，还能避免类型转换错误。本节将深入讲解 `auto`、`decltype` 和 `decltype(auto)` 的工作原理和使用场景。

---

## 1. auto 关键字

### 1.1 基本用法

```cpp
auto x = 42;           // int
auto y = 3.14;         // double
auto z = 'c';          // char
auto s = "hello";      // const char*
auto str = std::string("hello");  // std::string

// 复杂类型
std::map<std::string, std::vector<int>> data;
auto it = data.begin();  // 省去繁琐的迭代器类型
// std::map<std::string, std::vector<int>>::iterator
```

### 1.2 auto 的类型推断规则

`auto` 的推断规则与模板参数推断相同：

```cpp
int x = 10;
const int cx = 20;
const int& rx = x;

// 规则1：忽略引用
auto a = rx;    // a 是 int（不是 int&）
auto& b = rx;   // b 是 const int&

// 规则2：忽略顶层 const
auto c = cx;    // c 是 int（不是 const int）
const auto d = cx;  // d 是 const int

// 规则3：保留底层 const
const int* px = &x;
auto e = px;    // e 是 const int*

// 规则4：数组和函数退化为指针
int arr[10];
auto f = arr;   // f 是 int*（不是 int[10]）

void func(int);
auto g = func;  // g 是 void(*)(int)
```

### 1.3 auto 与引用

```cpp
int x = 10;

// auto（值）
auto a = x;     // int，拷贝

// auto&（左值引用）
auto& b = x;    // int&

// const auto&（常量左值引用）
const auto& c = x;  // const int&
const auto& d = 42; // const int&（可以绑定右值）

// auto&&（转发引用）
auto&& e = x;    // int&（x 是左值）
auto&& f = 42;   // int&&（42 是右值）
```

### 1.4 auto 与初始化列表

```cpp
// 注意：auto 与 {} 的特殊行为
auto x1 = 10;    // int
auto x2(10);     // int
auto x3{10};     // int（C++17 起）
auto x4 = {10};  // std::initializer_list<int>

// C++17 之前，x3 也是 std::initializer_list<int>
// C++17 修改了这个规则
```

### 1.5 auto 的使用场景

```cpp
// ✅ 好的使用场景

// 1. 迭代器
for (auto it = container.begin(); it != container.end(); ++it) {}

// 2. Lambda
auto lambda = [](int x) { return x * 2; };

// 3. 复杂类型
auto result = std::make_shared<std::map<std::string, std::vector<int>>>();

// 4. 范围 for
for (const auto& item : container) {}

// 5. 从函数返回类型推断
auto value = get_value();

// ⚠️ 谨慎使用的场景

// 1. 类型不明显时
auto x = foo();  // x 是什么类型？看不出来

// 2. 数值类型
auto size = container.size();  // size_t，但看起来像 int
auto index = 0;  // int，不是 size_t，可能导致符号问题
```

---

## 2. decltype

### 2.1 基本用法

`decltype` 推断表达式的类型，**不执行表达式**：

```cpp
int x = 10;
const int& rx = x;

decltype(x) a;     // int
decltype(rx) b = x; // const int&（保留引用和 const）

// decltype 用于获取表达式类型
decltype(x + 1) c; // int（x + 1 的类型）
```

### 2.2 decltype 与 auto 的区别

```cpp
int x = 10;
const int& rx = x;

// auto：忽略引用和顶层 const
auto a = rx;       // int

// decltype：保留引用和 const
decltype(rx) b = x; // const int&

// 另一个区别
const int cx = 20;
auto c = cx;       // int（忽略 const）
decltype(cx) d = 30; // const int（保留 const）
```

### 2.3 decltype 的特殊规则

```cpp
int x = 10;

// 规则：如果表达式是带括号的变量，结果是引用
decltype(x) a;     // int
decltype((x)) b = x; // int&（注意括号！）

// 原因：
// - decltype(变量名) 返回变量的声明类型
// - decltype((表达式)) 返回表达式的值类别对应的类型
//   - 左值表达式 → 左值引用
//   - 右值表达式 → 值类型
```

### 2.4 decltype 的常见用途

```cpp
// 1. 声明与表达式同类型的变量
std::vector<int> v;
decltype(v)::value_type x;  // int

// 2. 模板中使用
template<typename Container>
void process(Container& c) {
    decltype(c.begin()) it = c.begin();
    // ...
}

// 3. 返回类型推断（C++11 尾置返回类型）
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}
```

---

## 3. decltype(auto) (C++14)

### 3.1 结合 auto 和 decltype

```cpp
int x = 10;
int& rx = x;

// auto：忽略引用
auto a = rx;           // int

// decltype(auto)：保留引用
decltype(auto) b = rx; // int&

// 规则：decltype(auto) 使用 decltype 规则推断初始化表达式的类型
```

### 3.2 函数返回类型

```cpp
// 问题：auto 返回类型会丢失引用
int& get_ref();

auto bad() {
    return get_ref();  // 返回 int（拷贝）
}

// 解决：decltype(auto) 保留引用
decltype(auto) good() {
    return get_ref();  // 返回 int&
}
```

### 3.3 完美转发返回值

```cpp
template<typename F, typename... Args>
decltype(auto) invoke_and_forward(F&& f, Args&&... args) {
    return std::forward<F>(f)(std::forward<Args>(args)...);
    // 返回类型与 f 的返回类型完全一致
}
```

### 3.4 注意事项

```cpp
int x = 10;

// 小心括号！
decltype(auto) a = x;    // int
decltype(auto) b = (x);  // int&（因为 (x) 是左值表达式）

// 返回语句中也要注意
int& get_ref();
decltype(auto) dangerous() {
    int local = 42;
    return (local);  // 返回 int&，悬垂引用！
}
```

---

## 4. 结构化绑定 (C++17)

### 4.1 基本用法

```cpp
// 绑定 pair
std::pair<int, std::string> p{1, "one"};
auto [id, name] = p;  // id: int, name: std::string

// 绑定 tuple
std::tuple<int, double, std::string> t{1, 3.14, "hello"};
auto [i, d, s] = t;

// 绑定数组
int arr[3] = {1, 2, 3};
auto [a, b, c] = arr;

// 绑定结构体
struct Point { int x, y; };
Point pt{10, 20};
auto [x, y] = pt;
```

### 4.2 与引用结合

```cpp
std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}};

// 值拷贝
for (auto [name, score] : scores) {
    score = 100;  // 不影响原 map
}

// const 引用（推荐用于只读遍历）
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << std::endl;
}

// 非 const 引用（可修改）
for (auto& [name, score] : scores) {
    score += 10;  // 修改原 map
}
```

### 4.3 绑定返回值

```cpp
std::pair<bool, int> try_parse(const std::string& s);

// 使用结构化绑定
if (auto [success, value] = try_parse("42"); success) {
    std::cout << "Parsed: " << value << std::endl;
}
```

### 4.4 自定义类型支持

```cpp
// 要支持结构化绑定，需要：
// 1. tuple_size 特化
// 2. tuple_element 特化
// 3. get 函数

class MyPair {
public:
    int first;
    std::string second;
};

// 如果是简单聚合类型，自动支持
// 否则需要提供 get 等函数

// 简单结构体自动支持
struct Simple {
    int a;
    double b;
    std::string c;
};
auto [x, y, z] = Simple{1, 2.0, "three"};
```

---

## 5. 类模板参数推断 (CTAD, C++17)

### 5.1 基本用法

```cpp
// C++17 之前
std::pair<int, double> p1{1, 3.14};
std::vector<int> v1{1, 2, 3};

// C++17：自动推断模板参数
std::pair p2{1, 3.14};      // pair<int, double>
std::vector v2{1, 2, 3};    // vector<int>
std::tuple t{1, 3.14, "hello"};  // tuple<int, double, const char*>
```

### 5.2 推断指南 (Deduction Guide)

```cpp
template<typename T>
class MyContainer {
public:
    MyContainer(std::initializer_list<T> init);
    MyContainer(size_t count, T value);
};

// 推断指南
template<typename T>
MyContainer(std::initializer_list<T>) -> MyContainer<T>;

template<typename T>
MyContainer(size_t, T) -> MyContainer<T>;

// 使用
MyContainer c1{1, 2, 3};     // MyContainer<int>
MyContainer c2(5, 3.14);     // MyContainer<double>
```

### 5.3 标准库中的 CTAD

```cpp
// 标准库已经提供推断指南
std::vector v1{1, 2, 3};                    // vector<int>
std::optional opt{42};                      // optional<int>
std::unique_ptr ptr{new int(42)};           // ❌ 不工作
auto ptr = std::make_unique<int>(42);       // ✅ 使用 make 函数

// lock_guard
std::mutex m;
std::lock_guard lock{m};  // lock_guard<std::mutex>

// array
std::array arr{1, 2, 3, 4, 5};  // array<int, 5>
```

---

## 6. 概念与约束 (C++20)

### 6.1 auto 与 concepts

```cpp
#include <concepts>

// 约束 auto
void process(std::integral auto x) {
    std::cout << "Integral: " << x << std::endl;
}

void process(std::floating_point auto x) {
    std::cout << "Floating: " << x << std::endl;
}

process(42);    // Integral: 42
process(3.14);  // Floating: 3.14
```

### 6.2 约束返回类型

```cpp
// 返回类型约束
std::integral auto get_count() {
    return 42;
}

// 模板约束
template<typename T>
    requires std::integral<T>
T increment(T x) {
    return x + 1;
}
```

---

## 7. 最佳实践

### 7.1 何时使用 auto

```cpp
// ✅ 使用 auto
// 1. 类型明显或无关紧要
auto it = vec.begin();
auto lambda = [](int x) { return x * 2; };
auto ptr = std::make_shared<Widget>();

// 2. 避免重复类型
std::map<std::string, std::vector<int>> data;
auto& value = data["key"];  // 不用重复写长类型

// 3. 范围 for 循环
for (const auto& item : container) {}

// ❌ 避免使用 auto
// 1. 类型不明显，影响可读性
auto result = compute();  // result 是什么类型？

// 2. 需要明确的数值类型
auto size = 0;  // int，可能想要 size_t
size_t size = 0;  // 明确

// 3. 代理类型（如 vector<bool>::reference）
std::vector<bool> flags = {true, false, true};
auto flag = flags[0];  // 不是 bool！是代理对象
bool flag = flags[0];  // 这样更安全
```

### 7.2 AAA 风格 (Almost Always Auto)

一些人提倡几乎总是使用 auto：

```cpp
// AAA 风格
auto x = int{42};
auto s = std::string{"hello"};
auto p = std::make_unique<Widget>();

// 优点：声明在左边，初始化在右边，一致性好
// 缺点：某些情况下不够直观
```

### 7.3 decltype(auto) 的使用场景

```cpp
// 1. 完美转发返回值
template<typename F>
decltype(auto) call(F f) {
    return f();
}

// 2. 代理/包装类
template<typename T>
class Wrapper {
    T& ref_;
public:
    decltype(auto) get() { return ref_; }
};
```

---

## 📝 练习题

### 练习1：类型推断
给出以下代码中各变量的类型：
```cpp
int x = 10;
const int& rx = x;
int* px = &x;

auto a = x;
auto b = rx;
auto& c = rx;
auto d = px;
const auto e = x;
auto&& f = x;
auto&& g = 42;
```

### 练习2：decltype 练习
```cpp
int x = 10;
int& rx = x;
const int cx = 20;

decltype(x) a;
decltype(rx) b = x;
decltype(cx) c = 0;
decltype((x)) d = x;
```

### 练习3：结构化绑定
使用结构化绑定遍历 `std::map`，统计满足条件的键值对数量。

### 练习4：CTAD
使用 C++17 CTAD 简化以下代码：
```cpp
std::pair<int, std::string> p{1, "one"};
std::vector<double> v{1.0, 2.0, 3.0};
std::tuple<int, double, char> t{1, 2.0, 'a'};
```

---

## 💡 要点总结

1. **auto**：让编译器推断类型，规则类似模板参数推断
2. **decltype**：获取表达式的精确类型，保留引用和 const
3. **decltype(auto)**：结合两者，完美转发返回类型
4. **结构化绑定**（C++17）：方便地解构 pair/tuple/结构体
5. **CTAD**（C++17）：类模板参数可以自动推断
6. **使用 auto 简化代码**，但注意可读性
7. **注意 auto 会忽略引用和顶层 const**
8. **注意 decltype((x)) 会变成引用**

---

## ⏭️ 下一节

[2.6 编译期计算](./06_constexpr_compile.md) - 探索 constexpr 和编译期编程

