#include "hpc_utils.hpp"
#include <iostream>
#include <cmath>

namespace hpc_utils {

void vector_add(const std::vector<double>& a, const std::vector<double>& b, std::vector<double>& c) {
    size_t n = a.size();
    c.resize(n);
    // 这里我们假设已经开启了编译器的自动向量化
    for (size_t i = 0; i < n; ++i) {
        c[i] = a[i] + b[i];
    }
}

void print_head(const std::vector<double>& v, size_t n) {
    size_t limit = std::min(n, v.size());
    std::cout << "[ ";
    for (size_t i = 0; i < limit; ++i) {
        std::cout << v[i] << " ";
    }
    if (v.size() > limit) std::cout << "... ";
    std::cout << "]" << std::endl;
}

} // namespace hpc_utils
