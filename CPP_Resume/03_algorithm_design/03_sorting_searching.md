# 3.3 排序与查找

## 📖 本节概述

排序和查找是最基础、最重要的算法。理解这些经典算法的原理和实现，不仅能帮助你解决实际问题，还能培养算法思维。

---

## 1. 排序算法概览

| 算法 | 时间复杂度（平均） | 空间 | 稳定 | 特点 |
|------|-------------------|------|------|------|
| 冒泡排序 | O(n²) | O(1) | ✅ | 简单，效率低 |
| 选择排序 | O(n²) | O(1) | ❌ | 简单，交换次数少 |
| 插入排序 | O(n²) | O(1) | ✅ | 对近乎有序的数组高效 |
| 归并排序 | O(n log n) | O(n) | ✅ | 稳定，适合链表 |
| 快速排序 | O(n log n) | O(log n) | ❌ | 通常最快 |
| 堆排序 | O(n log n) | O(1) | ❌ | 原地，最坏情况有保证 |
| 计数排序 | O(n + k) | O(k) | ✅ | 适合小范围整数 |

---

## 2. 冒泡排序

### 2.1 原理

反复遍历数组，比较相邻元素，若顺序错误则交换。每轮遍历后，最大元素"冒泡"到末尾。

```
初始: [5, 3, 8, 4, 2]
第1轮: [3, 5, 4, 2, 8]  → 8 到末尾
第2轮: [3, 4, 2, 5, 8]  → 5 到倒数第二
第3轮: [3, 2, 4, 5, 8]
第4轮: [2, 3, 4, 5, 8]  → 完成
```

### 2.2 实现

```cpp
void bubble_sort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        // 优化：如果没有交换，说明已经有序
        if (!swapped) break;
    }
}
```

### 2.3 复杂度

- 时间：O(n²)，最好 O(n)（已有序时）
- 空间：O(1)
- 稳定：✅

---

## 3. 选择排序

### 3.1 原理

每轮选择未排序部分的最小元素，放到已排序部分的末尾。

```
初始:     [5, 3, 8, 4, 2]
选最小2:  [2, 3, 8, 4, 5]
选最小3:  [2, 3, 8, 4, 5]
选最小4:  [2, 3, 4, 8, 5]
选最小5:  [2, 3, 4, 5, 8]
```

### 3.2 实现

```cpp
void selection_sort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        int min_idx = i;
        for (int j = i + 1; j < n; ++j) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            std::swap(arr[i], arr[min_idx]);
        }
    }
}
```

### 3.3 复杂度

- 时间：O(n²)，任何情况
- 空间：O(1)
- 稳定：❌（交换可能破坏相对顺序）

---

## 4. 插入排序

### 4.1 原理

维护一个已排序的前缀。每次将下一个元素插入到前缀的正确位置。

```
初始:     [5, 3, 8, 4, 2]
插入3:    [3, 5, 8, 4, 2]
插入8:    [3, 5, 8, 4, 2]
插入4:    [3, 4, 5, 8, 2]
插入2:    [2, 3, 4, 5, 8]
```

### 4.2 实现

```cpp
void insertion_sort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        // 将大于 key 的元素后移
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            --j;
        }
        arr[j + 1] = key;
    }
}
```

### 4.3 复杂度

- 时间：O(n²)，最好 O(n)（已有序时）
- 空间：O(1)
- 稳定：✅

**适用场景**：小规模数据或近乎有序的数据。

---

## 5. 归并排序

### 5.1 原理

分治思想：
1. **分**：将数组分成两半
2. **治**：递归排序两半
3. **合**：合并两个有序数组

```
        [5, 3, 8, 4, 2, 7, 1, 6]
       /                        \
  [5, 3, 8, 4]              [2, 7, 1, 6]
   /       \                  /       \
[5, 3]   [8, 4]          [2, 7]   [1, 6]
 / \      / \             / \      / \
[5][3]  [8][4]          [2][7]  [1][6]
 \ /      \ /             \ /      \ /
[3, 5]   [4, 8]          [2, 7]  [1, 6]
   \       /                \       /
  [3, 4, 5, 8]          [1, 2, 6, 7]
       \                    /
   [1, 2, 3, 4, 5, 6, 7, 8]
```

### 5.2 实现

```cpp
void merge(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }
    
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    for (int i = 0; i < k; ++i) {
        arr[left + i] = temp[i];
    }
}

void merge_sort(std::vector<int>& arr, int left, int right) {
    if (left >= right) return;
    
    int mid = left + (right - left) / 2;
    merge_sort(arr, left, mid);
    merge_sort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

// 调用入口
void merge_sort(std::vector<int>& arr) {
    if (arr.empty()) return;
    merge_sort(arr, 0, arr.size() - 1);
}
```

### 5.3 复杂度

- 时间：O(n log n)，任何情况
- 空间：O(n)
- 稳定：✅

---

## 6. 快速排序

### 6.1 原理

分治思想：
1. 选择一个**基准元素**（pivot）
2. **分区**：将小于 pivot 的放左边，大于的放右边
3. **递归**：对左右两部分递归排序

### 6.2 实现

```cpp
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];  // 选择最后一个元素作为基准
    int i = low - 1;        // i 指向小于 pivot 区域的末尾
    
    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quick_sort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

// 调用入口
void quick_sort(std::vector<int>& arr) {
    if (arr.empty()) return;
    quick_sort(arr, 0, arr.size() - 1);
}
```

### 6.3 优化

```cpp
// 三数取中选择 pivot
int median_of_three(std::vector<int>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    if (arr[low] > arr[mid]) std::swap(arr[low], arr[mid]);
    if (arr[low] > arr[high]) std::swap(arr[low], arr[high]);
    if (arr[mid] > arr[high]) std::swap(arr[mid], arr[high]);
    std::swap(arr[mid], arr[high - 1]);
    return arr[high - 1];
}

// 小数组使用插入排序
void quick_sort_optimized(std::vector<int>& arr, int low, int high) {
    if (high - low < 10) {
        insertion_sort_range(arr, low, high);
        return;
    }
    // ... 正常快排
}
```

### 6.4 复杂度

- 时间：O(n log n) 平均，O(n²) 最坏（已有序时）
- 空间：O(log n)（递归栈）
- 稳定：❌

---

## 7. 堆排序

### 7.1 原理

1. 建立最大堆
2. 将堆顶（最大元素）与末尾交换
3. 缩小堆范围，重新堆化
4. 重复直到完成

### 7.2 实现

```cpp
void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest])
        largest = left;
    if (right < n && arr[right] > arr[largest])
        largest = right;
    
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heap_sort(std::vector<int>& arr) {
    int n = arr.size();
    
    // 建堆
    for (int i = n / 2 - 1; i >= 0; --i) {
        heapify(arr, n, i);
    }
    
    // 逐个提取最大元素
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
```

### 7.3 复杂度

- 时间：O(n log n)，任何情况
- 空间：O(1)
- 稳定：❌

---

## 8. 线性查找

```cpp
// O(n) 时间
int linear_search(const std::vector<int>& arr, int target) {
    for (size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == target) return i;
    }
    return -1;
}
```

---

## 9. 二分查找

### 9.1 基本二分

**前提**：数组已排序！

```cpp
int binary_search(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;  // 防止溢出
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```

### 9.2 查找边界

```cpp
// 查找第一个等于 target 的位置
int find_first(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    int result = -1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            result = mid;
            right = mid - 1;  // 继续向左查找
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return result;
}

// 查找最后一个等于 target 的位置
int find_last(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    int result = -1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            result = mid;
            left = mid + 1;  // 继续向右查找
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return result;
}
```

### 9.3 查找插入位置

```cpp
// 查找第一个 >= target 的位置（lower_bound）
int lower_bound(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}

// 查找第一个 > target 的位置（upper_bound）
int upper_bound(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] <= target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}
```

### 9.4 二分答案

```cpp
// 示例：在有序数组中找 >= sqrt(n) 的最小整数
int sqrt_int(int n) {
    if (n < 2) return n;
    
    int left = 1, right = n / 2;
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if ((long long)mid * mid < n) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return left * left == n ? left : left - 1;
}
```

---

## 10. 选择排序算法的建议

| 场景 | 推荐算法 |
|------|----------|
| 一般情况 | `std::sort`（快排变体） |
| 需要稳定排序 | `std::stable_sort`（归并） |
| 数据量小（< 50） | 插入排序 |
| 近乎有序 | 插入排序 |
| 只需要 Top K | `std::partial_sort` |
| 查找中位数 | `std::nth_element` |
| 内存受限 | 堆排序 |
| 小范围整数 | 计数排序 |

---

## 📝 练习题

### 练习1：实现双路快排
标准快排对于大量重复元素效率低，实现双路快排优化。

### 练习2：旋转数组查找
在旋转有序数组 `[4,5,6,7,0,1,2]` 中查找目标值。

### 练习3：找峰值元素
在数组中找一个峰值（比左右邻居都大）。

### 练习4：搜索二维矩阵
在行列有序的矩阵中查找目标值。

---

## 💡 要点总结

1. **O(n²) 算法**：冒泡、选择、插入 —— 小数据量或特定场景
2. **O(n log n) 算法**：归并、快排、堆排 —— 通用选择
3. **快排通常最快**，但最坏情况 O(n²)
4. **归并稳定**，但需要额外空间
5. **二分查找 O(log n)**，前提是有序
6. **实际应用使用 STL**：`std::sort`、`std::binary_search`

---

## ⏭️ 下一节

[3.4 递归与动态规划](./04_recursion_dp.md) - 掌握分治和 DP 思想

