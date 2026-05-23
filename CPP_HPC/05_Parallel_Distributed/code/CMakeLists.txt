cmake_minimum_required(VERSION 3.10)
project(Parallel_Distributed)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 MPI
find_package(MPI REQUIRED)

# 开启优化
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native)
endif()

# 1. Hello World
add_executable(mpi_hello mpi_hello.cpp)
target_link_libraries(mpi_hello PRIVATE MPI::MPI_CXX)

# 2. Point-to-Point (Ping Pong)
add_executable(mpi_p2p mpi_p2p.cpp)
target_link_libraries(mpi_p2p PRIVATE MPI::MPI_CXX)

# 3. Collective (PI)
add_executable(mpi_coll mpi_coll.cpp)
target_link_libraries(mpi_coll PRIVATE MPI::MPI_CXX)
