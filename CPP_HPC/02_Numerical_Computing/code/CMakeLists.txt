cmake_minimum_required(VERSION 3.14)
project(Numerical_Computing)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 优化选项
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native)
endif()

# 使用 FetchContent 自动下载并集成 Eigen
include(FetchContent)

message(STATUS "Fetching Eigen3...")
FetchContent_Declare(
  Eigen3
  URL      https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
)

# 注意：Eigen 是 header-only 库，这里只需 MakeAvailable 即可
FetchContent_MakeAvailable(Eigen3)

# 1. 浮点数精度测试
add_executable(float_precision float_precision.cpp)

# 2. Eigen 示例
add_executable(eigen_example eigen_example.cpp)
# 链接 Eigen 库 (实际上只是添加 include 路径)
target_link_libraries(eigen_example PRIVATE Eigen3::Eigen)
