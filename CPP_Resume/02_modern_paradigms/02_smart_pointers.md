# 2.2 智能指针详解

## 📖 本节概述

智能指针是现代 C++ 中管理动态内存的标准方式。它们是 RAII 原则的直接应用——将动态分配的内存包装在对象中，让对象的生命周期管理内存的生命周期。

**核心原则**：永远不要使用裸 `new` 和 `delete`，使用智能指针代替。

---

## 1. 为什么需要智能指针？

### 1.1 裸指针的问题

```cpp
void problems_with_raw_pointers() {
    // 问题1：忘记 delete
    int* p1 = new int(42);
    return;  // 内存泄漏！
    
    // 问题2：重复 delete
    int* p2 = new int(42);
    delete p2;
    delete p2;  // 未定义行为！
    
    // 问题3：悬垂指针
    int* p3 = new int(42);
    int* p4 = p3;
    delete p3;
    *p4 = 100;  // 访问已释放内存！
    
    // 问题4：异常导致泄漏
    int* p5 = new int(42);
    risky_operation();  // 如果抛出异常
    delete p5;          // 永远不会执行
}
```

### 1.2 智能指针的解决方案

```cpp
#include <memory>

void solution_with_smart_pointers() {
    // 自动释放，不会泄漏
    auto p1 = std::make_unique<int>(42);
    
    // 无法重复释放（不持有裸指针）
    // 编译期保证唯一所有权
    
    // 共享所有权时使用 shared_ptr
    auto p2 = std::make_shared<int>(42);
    auto p3 = p2;  // 引用计数 = 2
    // 两者离开作用域时正确释放
    
    // 异常安全
    auto p4 = std::make_unique<int>(42);
    risky_operation();  // 即使抛出异常
}  // 所有智能指针自动释放
```

---

## 2. std::unique_ptr - 独占所有权

### 2.1 基本用法

```cpp
#include <memory>
#include <iostream>

class Resource {
public:
    Resource(int id) : id_(id) {
        std::cout << "Resource " << id_ << " created" << std::endl;
    }
    ~Resource() {
        std::cout << "Resource " << id_ << " destroyed" << std::endl;
    }
    void use() { std::cout << "Using Resource " << id_ << std::endl; }
private:
    int id_;
};

void demo_unique_ptr() {
    // 创建 unique_ptr
    std::unique_ptr<Resource> p1 = std::make_unique<Resource>(1);  // 推荐
    std::unique_ptr<Resource> p2(new Resource(2));  // 也可以，但不推荐
    
    // 使用
    p1->use();
    (*p1).use();
    
    // 检查是否为空
    if (p1) {
        std::cout << "p1 is not null" << std::endl;
    }
    
    // 获取裸指针（不转移所有权）
    Resource* raw = p1.get();
    raw->use();
    
    // 释放所有权
    Resource* released = p1.release();  // p1 变为 nullptr
    delete released;  // 手动管理
    
    // 重置
    p2.reset();  // 释放并置空
    p2.reset(new Resource(3));  // 释放旧的，持有新的
    
}  // p2 离开作用域，自动释放
```

### 2.2 所有权转移

`unique_ptr` 不能拷贝，只能移动：

```cpp
void demo_move_unique_ptr() {
    auto p1 = std::make_unique<Resource>(1);
    
    // auto p2 = p1;  // ❌ 编译错误：不能拷贝
    auto p2 = std::move(p1);  // ✅ 移动所有权
    
    if (!p1) {
        std::cout << "p1 is now null" << std::endl;
    }
    p2->use();  // p2 拥有资源
}

// 从函数返回 unique_ptr
std::unique_ptr<Resource> create_resource(int id) {
    return std::make_unique<Resource>(id);  // 自动移动
}

// 接受 unique_ptr 参数（转移所有权）
void take_ownership(std::unique_ptr<Resource> p) {
    p->use();
}  // 函数结束时释放

void demo_transfer() {
    auto p = create_resource(42);  // 获取所有权
    take_ownership(std::move(p));  // 转移所有权
    // p 现在为空
}
```

### 2.3 unique_ptr 与数组

```cpp
void demo_unique_ptr_array() {
    // 管理数组
    std::unique_ptr<int[]> arr = std::make_unique<int[]>(10);
    
    // 使用下标访问
    for (int i = 0; i < 10; ++i) {
        arr[i] = i * 10;
    }
    
    // 注意：数组版本没有 operator* 和 operator->
    // std::cout << *arr;  // ❌ 错误
    
    std::cout << arr[0] << std::endl;  // ✅
    
}  // 自动 delete[]
```

### 2.4 自定义删除器

```cpp
#include <cstdio>

void demo_custom_deleter() {
    // 使用自定义删除器管理 FILE*
    auto file_deleter = [](FILE* f) {
        if (f) {
            std::cout << "Closing file" << std::endl;
            fclose(f);
        }
    };
    
    std::unique_ptr<FILE, decltype(file_deleter)> file(
        fopen("test.txt", "w"), 
        file_deleter
    );
    
    if (file) {
        fprintf(file.get(), "Hello, World!");
    }
}  // 自动 fclose

// 使用函数指针作为删除器
void close_file(FILE* f) {
    if (f) fclose(f);
}

void demo_function_deleter() {
    std::unique_ptr<FILE, decltype(&close_file)> file(
        fopen("test.txt", "w"),
        close_file
    );
}
```

---

## 3. std::shared_ptr - 共享所有权

### 3.1 基本用法

```cpp
#include <memory>

void demo_shared_ptr() {
    // 创建 shared_ptr
    std::shared_ptr<Resource> p1 = std::make_shared<Resource>(1);  // 推荐
    
    std::cout << "use_count: " << p1.use_count() << std::endl;  // 1
    
    // 共享所有权
    std::shared_ptr<Resource> p2 = p1;  // 拷贝
    std::cout << "use_count: " << p1.use_count() << std::endl;  // 2
    
    {
        std::shared_ptr<Resource> p3 = p1;
        std::cout << "use_count: " << p1.use_count() << std::endl;  // 3
    }  // p3 离开作用域
    
    std::cout << "use_count: " << p1.use_count() << std::endl;  // 2
    
    p2.reset();  // p2 放弃所有权
    std::cout << "use_count: " << p1.use_count() << std::endl;  // 1
    
}  // p1 离开作用域，引用计数归零，资源被释放
```

### 3.2 make_shared 的优势

```cpp
void demo_make_shared() {
    // 方式1：两次内存分配
    std::shared_ptr<Resource> p1(new Resource(1));
    // 1) new Resource 分配对象
    // 2) shared_ptr 内部分配控制块
    
    // 方式2：一次内存分配（推荐）
    auto p2 = std::make_shared<Resource>(2);
    // 对象和控制块一起分配，更高效
    
    // 异常安全
    // 如果这样写，可能泄漏：
    // process(std::shared_ptr<int>(new int(42)), riskyFunction());
    // 因为 new int 可能在 riskyFunction 之前执行，
    // 但 shared_ptr 构造在 riskyFunction 之后
    
    // make_shared 保证异常安全
    // process(std::make_shared<int>(42), riskyFunction());
}
```

### 3.3 shared_ptr 与多态

```cpp
class Base {
public:
    virtual ~Base() = default;
    virtual void speak() { std::cout << "Base" << std::endl; }
};

class Derived : public Base {
public:
    void speak() override { std::cout << "Derived" << std::endl; }
};

void demo_polymorphism() {
    std::shared_ptr<Base> p = std::make_shared<Derived>();
    p->speak();  // "Derived"
    
    // 向下转型
    std::shared_ptr<Derived> d = std::dynamic_pointer_cast<Derived>(p);
    if (d) {
        d->speak();
    }
    
    // 静态转型
    std::shared_ptr<Derived> d2 = std::static_pointer_cast<Derived>(p);
}
```

### 3.4 自定义删除器

```cpp
void demo_shared_ptr_deleter() {
    // shared_ptr 的删除器不影响类型
    auto deleter = [](Resource* r) {
        std::cout << "Custom deleter" << std::endl;
        delete r;
    };
    
    std::shared_ptr<Resource> p1(new Resource(1), deleter);
    std::shared_ptr<Resource> p2(new Resource(2), deleter);
    
    // p1 和 p2 类型相同，可以赋值
    p1 = p2;
    
    // 对比 unique_ptr：删除器是类型的一部分
    // std::unique_ptr<Resource, decltype(deleter)>
}
```

### 3.5 enable_shared_from_this

当类内部需要获取指向自身的 `shared_ptr` 时：

```cpp
class Widget : public std::enable_shared_from_this<Widget> {
public:
    void process() {
        // 获取指向自身的 shared_ptr
        std::shared_ptr<Widget> self = shared_from_this();
        // 可以安全地传递给其他函数
        async_operation(self);
    }
    
    static std::shared_ptr<Widget> create() {
        // 工厂函数确保对象由 shared_ptr 管理
        return std::make_shared<Widget>();
    }

private:
    Widget() = default;  // 私有构造函数
};

void demo_enable_shared_from_this() {
    auto w = Widget::create();
    w->process();
    
    // ❌ 错误用法：
    // Widget w2;
    // w2.shared_from_this();  // 未定义行为！对象不由 shared_ptr 管理
}
```

---

## 4. std::weak_ptr - 弱引用

### 4.1 为什么需要 weak_ptr

`shared_ptr` 的循环引用问题：

```cpp
class Node {
public:
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;  // ❌ 问题！
    
    ~Node() { std::cout << "Node destroyed" << std::endl; }
};

void demo_circular_reference() {
    auto node1 = std::make_shared<Node>();
    auto node2 = std::make_shared<Node>();
    
    node1->next = node2;
    node2->prev = node1;  // 循环引用！
    
    // node1 引用 node2，node2 引用 node1
    // 即使离开作用域，引用计数都不会归零
    // 内存泄漏！
}
```

### 4.2 使用 weak_ptr 打破循环

```cpp
class NodeFixed {
public:
    std::shared_ptr<NodeFixed> next;
    std::weak_ptr<NodeFixed> prev;  // ✅ 使用 weak_ptr
    
    ~NodeFixed() { std::cout << "NodeFixed destroyed" << std::endl; }
};

void demo_weak_ptr_solution() {
    auto node1 = std::make_shared<NodeFixed>();
    auto node2 = std::make_shared<NodeFixed>();
    
    node1->next = node2;
    node2->prev = node1;  // weak_ptr 不增加引用计数
    
    std::cout << "node1 use_count: " << node1.use_count() << std::endl;  // 1
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;  // 2
    
}  // 正确释放！
```

### 4.3 weak_ptr 的用法

```cpp
void demo_weak_ptr_usage() {
    std::shared_ptr<int> sp = std::make_shared<int>(42);
    std::weak_ptr<int> wp = sp;  // 从 shared_ptr 创建
    
    // weak_ptr 不能直接访问对象
    // *wp;  // ❌ 错误
    
    // 检查对象是否还存在
    if (!wp.expired()) {
        std::cout << "Object still exists" << std::endl;
    }
    
    // 获取 shared_ptr 来访问对象
    if (auto locked = wp.lock()) {  // 返回 shared_ptr
        std::cout << "Value: " << *locked << std::endl;
    } else {
        std::cout << "Object has been destroyed" << std::endl;
    }
    
    // 销毁 shared_ptr
    sp.reset();
    
    // 再次检查
    if (wp.expired()) {
        std::cout << "Object is gone" << std::endl;
    }
    
    auto locked = wp.lock();  // 返回空的 shared_ptr
    if (!locked) {
        std::cout << "lock() returned nullptr" << std::endl;
    }
}
```

### 4.4 weak_ptr 的应用场景

```cpp
// 1. 缓存
class Cache {
    std::unordered_map<int, std::weak_ptr<Resource>> cache_;
    
public:
    std::shared_ptr<Resource> get(int id) {
        auto it = cache_.find(id);
        if (it != cache_.end()) {
            if (auto sp = it->second.lock()) {
                return sp;  // 缓存命中
            }
            cache_.erase(it);  // 对象已销毁，清理缓存
        }
        
        // 缓存未命中，创建新对象
        auto sp = std::make_shared<Resource>(id);
        cache_[id] = sp;
        return sp;
    }
};

// 2. 观察者模式
class Observer : public std::enable_shared_from_this<Observer> {
public:
    virtual void notify() = 0;
    virtual ~Observer() = default;
};

class Subject {
    std::vector<std::weak_ptr<Observer>> observers_;
    
public:
    void attach(std::shared_ptr<Observer> obs) {
        observers_.push_back(obs);
    }
    
    void notify_all() {
        // 清理已销毁的观察者，通知存活的
        auto it = observers_.begin();
        while (it != observers_.end()) {
            if (auto obs = it->lock()) {
                obs->notify();
                ++it;
            } else {
                it = observers_.erase(it);
            }
        }
    }
};
```

---

## 5. 智能指针的最佳实践

### 5.1 选择正确的智能指针

```
需要共享所有权吗？
├─ 是 → shared_ptr
│       └─ 需要避免循环引用？→ weak_ptr
└─ 否 → unique_ptr（默认选择）
```

### 5.2 使用 make 函数

```cpp
// ✅ 推荐
auto p1 = std::make_unique<int>(42);
auto p2 = std::make_shared<int>(42);

// ❌ 不推荐
std::unique_ptr<int> p3(new int(42));
std::shared_ptr<int> p4(new int(42));
```

### 5.3 传递智能指针

```cpp
// 1. 传递 unique_ptr：转移所有权
void take_ownership(std::unique_ptr<Widget> widget);
take_ownership(std::move(my_widget));

// 2. 传递 shared_ptr：共享所有权
void share_ownership(std::shared_ptr<Widget> widget);
share_ownership(my_shared_widget);  // 拷贝，引用计数 +1

// 3. 只需要使用，不需要所有权：传递引用或裸指针
void just_use(Widget& widget);
void just_use(Widget* widget);
just_use(*my_widget);
just_use(my_widget.get());
```

### 5.4 从函数返回智能指针

```cpp
// 返回 unique_ptr：工厂模式
std::unique_ptr<Widget> create_widget() {
    return std::make_unique<Widget>();
}

// 返回 shared_ptr：需要共享时
std::shared_ptr<Widget> get_shared_widget() {
    static auto widget = std::make_shared<Widget>();
    return widget;
}
```

### 5.5 避免的做法

```cpp
// ❌ 不要从同一个裸指针创建多个智能指针
int* raw = new int(42);
std::shared_ptr<int> p1(raw);
std::shared_ptr<int> p2(raw);  // 双重释放！

// ❌ 不要将栈上对象交给智能指针
int stack_var = 42;
std::shared_ptr<int> p(&stack_var);  // 会尝试 delete 栈变量！

// ❌ 不要在构造函数中调用 shared_from_this
class Bad : public std::enable_shared_from_this<Bad> {
public:
    Bad() {
        auto self = shared_from_this();  // 未定义行为！
    }
};

// ✅ 使用工厂函数
class Good : public std::enable_shared_from_this<Good> {
    Good() = default;
public:
    static std::shared_ptr<Good> create() {
        return std::make_shared<Good>();
    }
    
    void init() {
        auto self = shared_from_this();  // OK
    }
};
```

---

## 6. 性能考量

### 6.1 unique_ptr vs shared_ptr

| 特性 | unique_ptr | shared_ptr |
|------|------------|------------|
| 大小 | 1个指针（或+删除器） | 2个指针 |
| 引用计数 | 无 | 有（原子操作） |
| 拷贝 | 不支持 | 支持 |
| 开销 | 接近裸指针 | 略高 |

### 6.2 make_shared 的内存布局

```cpp
// 使用 new
std::shared_ptr<int> p1(new int(42));
// 内存布局：
// [控制块] [int 对象]  ← 两次分配

// 使用 make_shared
auto p2 = std::make_shared<int>(42);
// 内存布局：
// [控制块 | int 对象]  ← 一次分配，更紧凑
```

### 6.3 注意 shared_ptr 的线程安全

```cpp
// 控制块的引用计数是线程安全的
std::shared_ptr<int> global_ptr = std::make_shared<int>(42);

void thread1() {
    auto local = global_ptr;  // ✅ 线程安全
}

void thread2() {
    auto local = global_ptr;  // ✅ 线程安全
}

// 但是修改 shared_ptr 本身不是线程安全的
void unsafe_thread() {
    global_ptr = std::make_shared<int>(100);  // ❌ 可能数据竞争
}

// 需要额外同步
std::mutex mtx;
void safe_thread() {
    std::lock_guard<std::mutex> lock(mtx);
    global_ptr = std::make_shared<int>(100);  // ✅
}
```

---

## 📝 练习题

### 练习1：资源池
使用 `shared_ptr` 和 `weak_ptr` 实现一个简单的对象池，支持对象复用。

### 练习2：双向链表
使用智能指针实现一个双向链表，注意避免循环引用。

### 练习3：文件管理器
创建一个 `unique_ptr` 包装的文件句柄类，支持移动但禁止拷贝。

### 练习4：简易 shared_ptr
自己实现一个简化版的 `shared_ptr`，理解引用计数的工作原理。

---

## 💡 要点总结

1. **默认使用 `unique_ptr`**：除非需要共享所有权
2. **使用 `make_unique` 和 `make_shared`**：更安全、更高效
3. **使用 `weak_ptr` 打破循环引用**：观察者模式、缓存等场景
4. **不需要所有权时传递引用或裸指针**：不要过度使用智能指针
5. **`shared_ptr` 的引用计数是原子的**：但对象本身不是线程安全的
6. **使用 `enable_shared_from_this`**：当需要从对象内部获取 `shared_ptr`

---

## ⏭️ 下一节

[2.3 移动语义与完美转发](./03_move_semantics.md) - 理解右值引用和 std::move

