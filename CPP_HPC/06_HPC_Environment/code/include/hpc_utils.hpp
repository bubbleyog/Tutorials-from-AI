#pragma once
#include <vector>

namespace hpc_utils {

// 一个简单的向量加法函数
void vector_add(const std::vector<double>& a, const std::vector<double>& b, std::vector<double>& c);

// 打印部分向量内容
void print_head(const std::vector<double>& v, size_t n = 5);

} // namespace hpc_utils
