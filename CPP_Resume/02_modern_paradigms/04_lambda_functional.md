# 2.4 Lambda 与函数式编程

## 📖 本节概述

Lambda 表达式是 C++11 引入的重要特性，它让我们可以在代码中内联定义匿名函数。结合 STL 算法，Lambda 使 C++ 具备了强大的函数式编程能力。

---

## 1. Lambda 基础

### 1.1 基本语法

```cpp
[捕获列表](参数列表) -> 返回类型 { 函数体 }
```

最简单的 Lambda：

```cpp
// 无参数、无捕获、无返回值
auto hello = []() { std::cout << "Hello!" << std::endl; };
hello();  // 调用

// 有参数
auto add = [](int a, int b) { return a + b; };
std::cout << add(3, 5) << std::endl;  // 8

// 显式指定返回类型
auto divide = [](double a, double b) -> double {
    if (b == 0) return 0;
    return a / b;
};
```

### 1.2 返回类型推断

```cpp
// 自动推断返回类型（单一 return 语句）
auto square = [](int x) { return x * x; };  // 返回 int

// 多个 return 语句，类型必须一致
auto abs_value = [](int x) {
    if (x < 0) return -x;
    return x;  // 都返回 int，OK
};

// 类型不一致需要显式指定
auto mixed = [](bool flag) -> double {
    if (flag) return 1;      // int
    return 3.14;             // double
};  // 需要 -> double
```

### 1.3 立即调用的 Lambda（IIFE）

```cpp
// 立即调用（Immediately Invoked Function Expression）
int result = [](int x) { return x * 2; }(21);
std::cout << result << std::endl;  // 42

// 用于复杂的初始化
const auto config = []() {
    Config c;
    c.load_from_file("config.json");
    c.validate();
    return c;
}();  // 立即调用，config 是 const
```

---

## 2. 捕获列表

捕获列表决定了 Lambda 如何访问外部变量。

### 2.1 值捕获

```cpp
int x = 10;
int y = 20;

// 捕获单个变量（值拷贝）
auto f1 = [x]() { return x; };

// 捕获多个变量
auto f2 = [x, y]() { return x + y; };

// 捕获所有使用的局部变量（值拷贝）
auto f3 = [=]() { return x + y; };

// 值捕获是拷贝！
x = 100;
std::cout << f1() << std::endl;  // 10（捕获时的值）
```

### 2.2 引用捕获

```cpp
int x = 10;

// 引用捕获单个变量
auto f1 = [&x]() { x = 100; };
f1();
std::cout << x << std::endl;  // 100

// 引用捕获所有变量
auto f2 = [&]() { x = 200; };

// 混合捕获
int y = 20;
auto f3 = [&x, y]() {  // x 引用捕获，y 值捕获
    x = 300;
    // y = 30;  // 错误：值捕获默认是 const
    return y;
};
```

### 2.3 mutable Lambda

值捕获的变量默认是 `const` 的，使用 `mutable` 可以修改：

```cpp
int x = 10;

// 默认：不能修改值捕获的变量
auto f1 = [x]() {
    // x = 20;  // 错误！
    return x;
};

// mutable：可以修改（但不影响外部变量）
auto f2 = [x]() mutable {
    x = 20;  // OK，修改的是 Lambda 内部的拷贝
    return x;
};

std::cout << f2() << std::endl;  // 20
std::cout << x << std::endl;     // 10（外部变量不变）
```

### 2.4 初始化捕获（C++14）

```cpp
// 移动捕获
auto ptr = std::make_unique<int>(42);
auto f1 = [p = std::move(ptr)]() {
    return *p;
};
// ptr 现在为空

// 自定义名称
int x = 10;
auto f2 = [value = x * 2]() {
    return value;  // 20
};

// 捕获表达式
auto f3 = [s = std::string("hello")]() {
    return s.size();
};
```

### 2.5 捕获 this

```cpp
class Widget {
    int value_ = 42;
    
public:
    auto get_lambda_v1() {
        // 捕获 this 指针
        return [this]() { return value_; };
    }
    
    auto get_lambda_v2() {
        // C++14：捕获 *this（拷贝整个对象）
        return [*this]() { return value_; };
    }
    
    auto get_lambda_v3() {
        // C++17：[=, this] 明确捕获 this
        return [=, this]() { return value_; };
    }
};

void demo() {
    auto lambda = [w = Widget()]() {
        return w.get_lambda_v1()();
    };
}
```

### 2.6 捕获列表总结

| 语法 | 含义 |
|------|------|
| `[]` | 不捕获任何变量 |
| `[x]` | 值捕获 x |
| `[&x]` | 引用捕获 x |
| `[=]` | 值捕获所有使用的局部变量 |
| `[&]` | 引用捕获所有使用的局部变量 |
| `[=, &x]` | 默认值捕获，x 引用捕获 |
| `[&, x]` | 默认引用捕获，x 值捕获 |
| `[this]` | 捕获 this 指针 |
| `[*this]` | 捕获 this 对象的拷贝（C++17） |
| `[x = expr]` | 初始化捕获（C++14） |

---

## 3. 泛型 Lambda（C++14）

### 3.1 auto 参数

```cpp
// C++14：参数可以是 auto
auto add = [](auto a, auto b) { return a + b; };

std::cout << add(1, 2) << std::endl;      // 3
std::cout << add(1.5, 2.5) << std::endl;  // 4.0
std::cout << add(std::string("Hello, "), std::string("World")) << std::endl;

// 等价于模板
// template<typename T, typename U>
// auto add(T a, U b) { return a + b; }
```

### 3.2 泛型 Lambda 的应用

```cpp
#include <vector>
#include <algorithm>

void demo_generic_lambda() {
    std::vector<int> ints = {3, 1, 4, 1, 5};
    std::vector<std::string> strings = {"banana", "apple", "cherry"};
    
    // 通用的打印函数
    auto print = [](const auto& container) {
        for (const auto& item : container) {
            std::cout << item << " ";
        }
        std::cout << std::endl;
    };
    
    print(ints);     // 3 1 4 1 5
    print(strings);  // banana apple cherry
    
    // 通用的排序比较器
    auto compare_desc = [](const auto& a, const auto& b) {
        return a > b;
    };
    
    std::sort(ints.begin(), ints.end(), compare_desc);
    std::sort(strings.begin(), strings.end(), compare_desc);
    
    print(ints);     // 5 4 3 1 1
    print(strings);  // cherry banana apple
}
```

---

## 4. C++20 Lambda 增强

### 4.1 模板 Lambda

```cpp
// C++20：显式模板参数
auto add = []<typename T>(T a, T b) {
    return a + b;
};

// 约束模板参数
auto add_numeric = []<typename T>
    requires std::is_arithmetic_v<T>
(T a, T b) {
    return a + b;
};

// 使用概念
auto print = []<std::integral T>(T value) {
    std::cout << "Integer: " << value << std::endl;
};
```

### 4.2 Lambda 的默认构造（C++20）

```cpp
// C++20：无捕获 Lambda 可以默认构造
auto lambda = [](int x) { return x * 2; };
decltype(lambda) another;  // C++20 OK，之前是错误

// 可以用于作为默认模板参数
template<typename Func = decltype([](int x) { return x; })>
void process(Func f = {}) {
    std::cout << f(42) << std::endl;
}
```

### 4.3 捕获参数包

```cpp
// C++20：捕获参数包
template<typename... Args>
auto make_tuple_lambda(Args... args) {
    return [...args = std::move(args)]() {
        return std::make_tuple(args...);
    };
}
```

---

## 5. Lambda 与 STL 算法

### 5.1 常用算法示例

```cpp
#include <vector>
#include <algorithm>
#include <numeric>

void demo_stl_algorithms() {
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // for_each：遍历
    std::for_each(nums.begin(), nums.end(), [](int n) {
        std::cout << n << " ";
    });
    std::cout << std::endl;
    
    // transform：变换
    std::vector<int> squares(nums.size());
    std::transform(nums.begin(), nums.end(), squares.begin(),
                   [](int n) { return n * n; });
    
    // count_if：计数
    int even_count = std::count_if(nums.begin(), nums.end(),
                                    [](int n) { return n % 2 == 0; });
    std::cout << "Even count: " << even_count << std::endl;
    
    // find_if：查找
    auto it = std::find_if(nums.begin(), nums.end(),
                           [](int n) { return n > 5; });
    if (it != nums.end()) {
        std::cout << "First > 5: " << *it << std::endl;
    }
    
    // remove_if + erase：删除
    nums.erase(
        std::remove_if(nums.begin(), nums.end(),
                       [](int n) { return n % 2 == 0; }),
        nums.end()
    );  // 删除所有偶数
    
    // accumulate：累加
    int sum = std::accumulate(nums.begin(), nums.end(), 0,
                              [](int acc, int n) { return acc + n; });
    
    // sort：排序
    std::sort(nums.begin(), nums.end(),
              [](int a, int b) { return a > b; });  // 降序
    
    // any_of / all_of / none_of
    bool has_negative = std::any_of(nums.begin(), nums.end(),
                                     [](int n) { return n < 0; });
    bool all_positive = std::all_of(nums.begin(), nums.end(),
                                     [](int n) { return n > 0; });
}
```

### 5.2 带状态的 Lambda

```cpp
void demo_stateful_lambda() {
    // 计数器
    int count = 0;
    std::vector<int> nums = {1, 2, 3, 4, 5};
    
    std::for_each(nums.begin(), nums.end(), [&count](int n) {
        if (n % 2 == 0) ++count;
    });
    std::cout << "Even count: " << count << std::endl;
    
    // 累加器
    int sum = 0;
    std::for_each(nums.begin(), nums.end(), [&sum](int n) {
        sum += n;
    });
    std::cout << "Sum: " << sum << std::endl;
    
    // mutable 状态
    auto counter = [n = 0]() mutable { return ++n; };
    std::cout << counter() << std::endl;  // 1
    std::cout << counter() << std::endl;  // 2
    std::cout << counter() << std::endl;  // 3
}
```

---

## 6. std::function

### 6.1 类型擦除的函数包装器

```cpp
#include <functional>

// std::function 可以存储任何可调用对象
std::function<int(int, int)> func;

// Lambda
func = [](int a, int b) { return a + b; };
std::cout << func(3, 5) << std::endl;  // 8

// 普通函数
int multiply(int a, int b) { return a * b; }
func = multiply;
std::cout << func(3, 5) << std::endl;  // 15

// 函数对象
struct Divider {
    int operator()(int a, int b) const { return a / b; }
};
func = Divider{};
std::cout << func(10, 3) << std::endl;  // 3
```

### 6.2 作为参数类型

```cpp
// 接受任何返回 int、接受两个 int 的可调用对象
void apply(std::function<int(int, int)> op, int a, int b) {
    std::cout << "Result: " << op(a, b) << std::endl;
}

void demo() {
    apply([](int a, int b) { return a + b; }, 3, 5);
    apply([](int a, int b) { return a * b; }, 3, 5);
    apply([](int a, int b) { return a - b; }, 3, 5);
}
```

### 6.3 std::function 的开销

```cpp
// std::function 有运行时开销（类型擦除、可能的堆分配）
// 如果性能敏感，使用模板：

// 使用 std::function（有开销）
void apply_v1(std::function<int(int)> f, int x);

// 使用模板（无开销，但不能存储）
template<typename F>
void apply_v2(F f, int x);

// 使用 auto（C++20）
void apply_v3(auto f, int x);
```

---

## 7. 高阶函数

### 7.1 返回 Lambda

```cpp
// 函数返回 Lambda
auto make_multiplier(int factor) {
    return [factor](int x) { return x * factor; };
}

void demo() {
    auto times2 = make_multiplier(2);
    auto times10 = make_multiplier(10);
    
    std::cout << times2(5) << std::endl;   // 10
    std::cout << times10(5) << std::endl;  // 50
}
```

### 7.2 组合函数

```cpp
// 函数组合：(f ∘ g)(x) = f(g(x))
template<typename F, typename G>
auto compose(F f, G g) {
    return [=](auto x) { return f(g(x)); };
}

void demo() {
    auto add1 = [](int x) { return x + 1; };
    auto times2 = [](int x) { return x * 2; };
    
    auto add1_then_times2 = compose(times2, add1);
    // add1_then_times2(5) = times2(add1(5)) = times2(6) = 12
    
    std::cout << add1_then_times2(5) << std::endl;  // 12
}
```

### 7.3 柯里化

```cpp
// 柯里化：将多参数函数转换为单参数函数链
auto curry_add = [](int a) {
    return [a](int b) {
        return a + b;
    };
};

void demo() {
    auto add5 = curry_add(5);
    std::cout << add5(3) << std::endl;  // 8
    std::cout << curry_add(10)(20) << std::endl;  // 30
}
```

### 7.4 部分应用

```cpp
#include <functional>

int add(int a, int b, int c) {
    return a + b + c;
}

void demo() {
    using namespace std::placeholders;
    
    // std::bind 进行部分应用
    auto add5 = std::bind(add, 5, _1, _2);
    std::cout << add5(3, 2) << std::endl;  // 10
    
    // Lambda 方式（更清晰）
    auto add5_lambda = [](int b, int c) { return add(5, b, c); };
    std::cout << add5_lambda(3, 2) << std::endl;  // 10
}
```

---

## 8. 实用技巧

### 8.1 递归 Lambda

```cpp
// 方法1：使用 std::function（有开销）
std::function<int(int)> factorial = [&factorial](int n) -> int {
    return n <= 1 ? 1 : n * factorial(n - 1);
};

// 方法2：使用泛型 Lambda 和 Y 组合子（复杂但无开销）
auto factorial2 = [](auto&& self, int n) -> int {
    return n <= 1 ? 1 : n * self(self, n - 1);
};
// 调用：factorial2(factorial2, 5)

// 方法3：C++23 deducing this（最优雅）
// auto factorial3 = [](this auto&& self, int n) -> int {
//     return n <= 1 ? 1 : n * self(n - 1);
// };
```

### 8.2 Lambda 作为比较器

```cpp
#include <set>
#include <map>

void demo() {
    // set 使用自定义比较器
    auto compare = [](int a, int b) { return a > b; };  // 降序
    std::set<int, decltype(compare)> s(compare);
    s.insert(1);
    s.insert(2);
    s.insert(3);
    // s: {3, 2, 1}
    
    // C++20：无捕获 Lambda 可以默认构造
    std::set<int, decltype([](int a, int b) { return a > b; })> s2;
}
```

### 8.3 Lambda 重载

```cpp
// 使用继承实现 Lambda 重载
template<typename... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};

// C++17 推断指南
template<typename... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

void demo() {
    auto visitor = overloaded{
        [](int i) { std::cout << "int: " << i << std::endl; },
        [](double d) { std::cout << "double: " << d << std::endl; },
        [](const std::string& s) { std::cout << "string: " << s << std::endl; }
    };
    
    visitor(42);
    visitor(3.14);
    visitor(std::string("hello"));
    
    // 常用于 std::variant
    std::variant<int, double, std::string> v = 42;
    std::visit(visitor, v);
}
```

---

## 📝 练习题

### 练习1：实现 map 函数
实现一个 `my_map` 函数，接受容器和 Lambda，返回变换后的新容器。

### 练习2：实现 filter 函数
实现一个 `my_filter` 函数，接受容器和谓词 Lambda，返回满足条件的元素。

### 练习3：实现 reduce 函数
实现一个 `my_reduce` 函数，类似于 `std::accumulate`。

### 练习4：实现 pipe
实现一个 `pipe` 函数，将多个函数组合成管道：
```cpp
auto result = pipe(x, f1, f2, f3);  // f3(f2(f1(x)))
```

---

## 💡 要点总结

1. **Lambda 语法**：`[捕获](参数) -> 返回类型 { 函数体 }`
2. **捕获方式**：值捕获 `[=]`、引用捕获 `[&]`、混合捕获
3. **mutable**：允许修改值捕获的变量
4. **初始化捕获**（C++14）：`[x = expr]` 支持移动捕获
5. **泛型 Lambda**（C++14）：使用 `auto` 参数
6. **模板 Lambda**（C++20）：显式模板参数
7. **std::function**：类型擦除的函数包装器，有开销
8. **Lambda 是现代 C++ 的核心工具**，广泛用于 STL 算法

---

## ⏭️ 下一节

[2.5 类型推断](./05_type_deduction.md) - 深入理解 auto 和 decltype

