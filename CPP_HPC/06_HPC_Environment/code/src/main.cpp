#include <iostream>
#include <vector>
#include "hpc_utils.hpp"

// 一个演示 CMake 项目结构的示例程序
// 即使代码很简单，我们也要演示规范的目录结构：
// include/  - 头文件
// src/      - 源代码
// CMakeLists.txt - 构建脚本

int main() {
    std::cout << "HPC Project Template" << std::endl;

    const size_t N = 1000;
    std::vector<double> a(N, 1.0);
    std::vector<double> b(N, 2.0);
    std::vector<double> c;

    hpc_utils::vector_add(a, b, c);

    std::cout << "Result preview: ";
    hpc_utils::print_head(c);

    return 0;
}
