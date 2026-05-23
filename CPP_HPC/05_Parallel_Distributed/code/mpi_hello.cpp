#include <mpi.h>
#include <iostream>
#include <vector>

// MPI Hello World
// 演示基本的 MPI 初始化、Rank 获取和终止

int main(int argc, char** argv) {
    // 1. 初始化 MPI 环境
    MPI_Init(&argc, &argv);

    // 2. 获取总进程数 (Size) 和当前进程 ID (Rank)
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // 3. 获取处理器名称 (通常是主机名)
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // 每个进程都会执行这行打印
    // 注意：打印顺序是不确定的，除非手动同步
    printf("Hello world from processor %s, rank %d out of %d processors\n",
           processor_name, world_rank, world_size);

    // 4. 终止 MPI 环境
    MPI_Finalize();
    return 0;
}
