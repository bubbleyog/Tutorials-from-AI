cmake_minimum_required(VERSION 3.10)
project(HPC_Project_Template VERSION 1.0.0 LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置构建类型（默认为 Release 以获得最高性能）
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# 设置 HPC 常用的编译器选项
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native -Wall -Wextra)
endif()

# 包含头文件目录
include_directories(include)

# 创建库 (Library)
# 将核心逻辑封装为库是良好的实践
add_library(hpc_core src/hpc_utils.cpp)

# 创建可执行文件 (Executable)
add_executable(app src/main.cpp)

# 链接库
target_link_libraries(app PRIVATE hpc_core)

# 安装规则 (可选，用于 make install)
install(TARGETS app DESTINATION bin)
install(TARGETS hpc_core DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)
