# 1.2 指针与引用

## 📖 本节概述

指针和引用是C++区别于其他高级语言的重要特性，也是理解C++内存模型的关键。本节将帮助你重新理解这两个核心概念，并学习如何在现代C++中正确使用它们。

---

## 1. 指针基础

### 1.1 什么是指针

指针是一个变量，它存储另一个变量的**内存地址**。

```cpp
int value = 42;
int* ptr = &value;  // ptr 存储 value 的地址

std::cout << "value 的值: " << value << std::endl;      // 42
std::cout << "value 的地址: " << &value << std::endl;   // 0x7fff...
std::cout << "ptr 的值: " << ptr << std::endl;          // 0x7fff... (同上)
std::cout << "ptr 指向的值: " << *ptr << std::endl;     // 42
```

### 1.2 指针的声明与初始化

```cpp
// 声明指针的几种写法（风格不同，效果相同）
int* p1;    // 推荐：强调 p1 是 int* 类型
int *p2;    // C风格
int * p3;   // 也可以

// ⚠️ 注意：声明多个指针时的陷阱
int* a, b;   // a 是指针，b 是 int！
int *a, *b;  // 两个都是指针

// 推荐：每行只声明一个指针
int* a;
int* b;

// 初始化
int* p4 = nullptr;    // C++11：使用 nullptr，不要用 NULL 或 0
int* p5 = &value;     // 指向已存在的变量
int* p6{nullptr};     // 列表初始化
```

### 1.3 指针操作

```cpp
int x = 10;
int* p = &x;

// 解引用：获取指针指向的值
int y = *p;     // y = 10

// 通过指针修改值
*p = 20;        // x 变为 20

// 指针重新赋值
int z = 30;
p = &z;         // p 现在指向 z
```

### 1.4 空指针

```cpp
// C++11 之前
int* p1 = NULL;   // 不推荐
int* p2 = 0;      // 不推荐

// C++11 推荐
int* p3 = nullptr;

// 检查空指针
if (p3 == nullptr) {
    std::cout << "指针为空" << std::endl;
}

// 更简洁的写法
if (!p3) {
    std::cout << "指针为空" << std::endl;
}

if (p3) {
    std::cout << "指针非空，值为: " << *p3 << std::endl;
}
```

> 💡 **为什么用 nullptr 而不是 NULL？**
> 
> `NULL` 通常被定义为 `0`，在某些情况下会导致重载解析问题：
> ```cpp
> void foo(int);
> void foo(int*);
> 
> foo(NULL);     // 调用哪个？可能是 foo(int)！
> foo(nullptr);  // 明确调用 foo(int*)
> ```

---

## 2. 指针与数组

### 2.1 数组名与指针

```cpp
int arr[5] = {1, 2, 3, 4, 5};

// 数组名在大多数情况下会退化为指向首元素的指针
int* p = arr;        // 等价于 int* p = &arr[0];

std::cout << *p << std::endl;      // 1
std::cout << arr[0] << std::endl;  // 1
std::cout << p[0] << std::endl;    // 1（指针也可以用下标）
```

### 2.2 指针算术

```cpp
int arr[5] = {10, 20, 30, 40, 50};
int* p = arr;

// 指针加减
std::cout << *p << std::endl;       // 10
std::cout << *(p + 1) << std::endl; // 20
std::cout << *(p + 2) << std::endl; // 30

// 遍历数组
for (int* ptr = arr; ptr < arr + 5; ++ptr) {
    std::cout << *ptr << " ";
}
// 输出：10 20 30 40 50

// 指针相减（得到元素个数差）
int* start = arr;
int* end = arr + 5;
std::ptrdiff_t diff = end - start;  // 5
```

### 2.3 指针与 C 风格字符串

```cpp
// C 风格字符串是 char 数组
const char* str = "Hello";  // 字符串字面量

// 遍历字符串
for (const char* p = str; *p != '\0'; ++p) {
    std::cout << *p;
}

// 现代C++：使用 std::string
std::string modern_str = "Hello";  // 推荐
```

---

## 3. 引用

### 3.1 什么是引用

引用是变量的**别名**。一旦初始化后，引用就和原变量绑定，无法再指向其他变量。

```cpp
int original = 42;
int& ref = original;  // ref 是 original 的引用（别名）

std::cout << original << std::endl;  // 42
std::cout << ref << std::endl;       // 42

ref = 100;  // 修改 ref 就是修改 original
std::cout << original << std::endl;  // 100

// 引用与原变量地址相同
std::cout << &original << std::endl;  // 0x7fff...
std::cout << &ref << std::endl;       // 0x7fff... (相同)
```

### 3.2 引用的特点

```cpp
// 1. 必须在声明时初始化
int& ref1;        // ❌ 错误：引用必须初始化
int& ref2 = x;    // ✅ 正确

// 2. 一旦绑定，不能更改
int a = 10, b = 20;
int& ref = a;
ref = b;          // 这是赋值，不是重新绑定！a 变为 20

// 3. 没有空引用
int& ref = nullptr;  // ❌ 错误：引用不能为空

// 4. 没有引用的引用
int&& rref;       // 这是右值引用，不是引用的引用
```

### 3.3 引用 vs 指针

| 特性 | 引用 | 指针 |
|------|------|------|
| 必须初始化 | ✅ 是 | ❌ 否 |
| 可以为空 | ❌ 否 | ✅ 是 |
| 可以重新绑定 | ❌ 否 | ✅ 是 |
| 语法 | 直接使用 | 需要 `*` 和 `&` |
| 可以有多级 | ❌ 否 | ✅ 是（`int**`） |

```cpp
// 使用场景对比
void modify_ptr(int* p) {
    if (p != nullptr) {  // 需要检查空指针
        *p = 100;
    }
}

void modify_ref(int& r) {
    r = 100;  // 不需要检查，引用永远有效
}
```

---

## 4. const 与指针/引用

### 4.1 const 指针

```cpp
int x = 10, y = 20;

// 1. 指向 const 的指针（底层 const）
// 不能通过指针修改值，但指针本身可以改
const int* p1 = &x;
// *p1 = 100;    // ❌ 错误
p1 = &y;         // ✅ 可以

// 等价写法
int const* p2 = &x;

// 2. const 指针（顶层 const）
// 指针本身不能改，但可以通过指针修改值
int* const p3 = &x;
*p3 = 100;       // ✅ 可以
// p3 = &y;      // ❌ 错误

// 3. 指向 const 的 const 指针
// 两者都不能改
const int* const p4 = &x;
// *p4 = 100;    // ❌ 错误
// p4 = &y;      // ❌ 错误
```

> 💡 **记忆技巧**：从右向左读
> - `const int*` → "pointer to const int"
> - `int* const` → "const pointer to int"
> - `const int* const` → "const pointer to const int"

### 4.2 const 引用

```cpp
int x = 10;

// const 引用：不能通过引用修改值
const int& cref = x;
// cref = 20;  // ❌ 错误

// const 引用可以绑定到临时对象
const int& temp_ref = 42;      // ✅ 可以
const std::string& s = "hello"; // ✅ 可以

// 非 const 引用不能绑定临时对象
// int& ref = 42;              // ❌ 错误
```

### 4.3 函数参数中的 const

```cpp
// 传值：拷贝，const 无意义（参数是拷贝）
void func1(int x);
void func1(const int x);  // 与上面等价

// 传引用：推荐对只读参数使用 const 引用
void func2(const std::string& s);  // 推荐：避免拷贝，禁止修改

// 传指针：根据需要选择
void func3(const int* p);     // 不能修改指向的值
void func4(int* const p);     // 不能修改指针本身
void func5(const int* const p); // 两者都不能改
```

---

## 5. 动态内存分配

### 5.1 new 和 delete

```cpp
// 分配单个对象
int* p = new int;          // 未初始化
int* p2 = new int(42);     // 初始化为 42
int* p3 = new int{42};     // C++11 列表初始化

delete p;
delete p2;
delete p3;

// 分配数组
int* arr = new int[10];           // 未初始化
int* arr2 = new int[10]();        // 零初始化
int* arr3 = new int[5]{1, 2, 3};  // C++11 初始化

delete[] arr;   // ⚠️ 注意：数组用 delete[]
delete[] arr2;
delete[] arr3;

// ❌ 常见错误
// delete arr;       // 应该用 delete[]
// delete[] p;       // 应该用 delete
```

### 5.2 内存泄漏

```cpp
void memory_leak() {
    int* p = new int(42);
    // 忘记 delete p;
    // 函数结束，p 被销毁，但内存没有释放！
}

void correct_way() {
    int* p = new int(42);
    // 使用 p...
    delete p;  // 释放内存
    p = nullptr;  // 好习惯：防止野指针
}
```

### 5.3 现代C++：智能指针（预告）

```cpp
#include <memory>

// 现代C++推荐使用智能指针，自动管理内存
std::unique_ptr<int> p1 = std::make_unique<int>(42);  // C++14
std::shared_ptr<int> p2 = std::make_shared<int>(42);

// 不需要手动 delete！离开作用域自动释放
// 详见第二章：现代编程范式
```

---

## 6. 指针的高级用法

### 6.1 指向指针的指针

```cpp
int x = 10;
int* p = &x;
int** pp = &p;

std::cout << x << std::endl;     // 10
std::cout << *p << std::endl;    // 10
std::cout << **pp << std::endl;  // 10

// 修改
**pp = 20;  // x 变为 20
```

### 6.2 函数指针

```cpp
// 普通函数
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int main() {
    // 声明函数指针
    int (*operation)(int, int);
    
    operation = add;
    std::cout << operation(5, 3) << std::endl;  // 8
    
    operation = subtract;
    std::cout << operation(5, 3) << std::endl;  // 2
    
    // 使用类型别名简化
    using BinaryOp = int(*)(int, int);
    BinaryOp op = add;
    std::cout << op(10, 20) << std::endl;  // 30
    
    return 0;
}
```

### 6.3 回调函数

```cpp
#include <vector>
#include <algorithm>

// 比较函数
bool compare_desc(int a, int b) {
    return a > b;
}

int main() {
    std::vector<int> nums = {3, 1, 4, 1, 5, 9, 2, 6};
    
    // 使用函数指针作为回调
    std::sort(nums.begin(), nums.end(), compare_desc);
    
    // 现代C++：使用 lambda 更简洁
    std::sort(nums.begin(), nums.end(), [](int a, int b) {
        return a > b;
    });
    
    return 0;
}
```

---

## 7. 右值引用（C++11 预览）

右值引用是C++11引入的重要特性，用于实现移动语义。这里只做简单介绍，详细内容见第二章。

### 7.1 左值与右值

```cpp
int x = 10;      // x 是左值，10 是右值

// 左值：有名字、有地址、可以取地址
int* p = &x;     // ✅ 可以取 x 的地址

// 右值：临时的、没有名字、不能取地址
// int* p2 = &10;  // ❌ 错误：不能取字面量的地址
// int* p3 = &(x + 1);  // ❌ 错误：不能取临时值的地址
```

### 7.2 右值引用语法

```cpp
int x = 10;

int& lref = x;      // 左值引用
// int& lref2 = 10;  // ❌ 错误：不能绑定到右值

int&& rref = 10;    // 右值引用：可以绑定到右值
int&& rref2 = x + 1;  // ✅ 可以

// const 左值引用可以绑定到右值（特殊规则）
const int& cref = 10;  // ✅ 可以
```

### 7.3 移动语义预览

```cpp
#include <string>
#include <utility>

std::string create_string() {
    return "Hello, World!";
}

int main() {
    // 传统拷贝
    std::string s1 = "Hello";
    std::string s2 = s1;  // 拷贝

    // 移动（C++11）
    std::string s3 = std::move(s1);  // s1 的资源被"移动"到 s3
    // s1 现在处于有效但未指定的状态
    
    // 从临时对象自动移动
    std::string s4 = create_string();  // 自动使用移动构造
    
    return 0;
}
```

> 💡 详细的移动语义和完美转发将在第二章深入讲解。

---

## 📝 练习题

### 练习1：交换两个整数
编写一个函数，使用指针交换两个整数的值。再编写一个使用引用的版本。

### 练习2：数组求和
编写一个函数，接受一个 int 数组和大小，返回所有元素的和。使用指针遍历。

### 练习3：查找最大值
编写一个函数，接受一个 int 数组和大小，返回指向最大元素的指针。

### 练习4：动态数组
创建一个动态分配的 int 数组，让用户输入元素，然后打印它们，最后正确释放内存。

---

## 💡 要点总结

1. **使用 nullptr**：不要使用 NULL 或 0 表示空指针
2. **优先使用引用**：当不需要重新绑定和空值时
3. **const 正确性**：使用 const 保护不应修改的数据
4. **避免裸指针管理内存**：使用智能指针（见第二章）
5. **注意数组的 delete[]**：分配数组用 `new[]`，释放用 `delete[]`
6. **检查指针有效性**：使用前确保指针非空
7. **避免悬垂指针**：delete 后将指针设为 nullptr

---

## ⏭️ 下一节

[1.3 类与对象](./03_classes_objects.md) - C++面向对象编程的核心

