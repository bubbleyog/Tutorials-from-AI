#include <mpi.h>
#include <iostream>
#include <cmath>

// MPI Collective Communication
// 使用 MPI_Reduce 和 MPI_Bcast 计算 PI
// 集合通信涉及通信域中的所有进程

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    long num_steps = 0;

    // 1. 只有 Rank 0 知道我们要算多少步
    if (world_rank == 0) {
        num_steps = 100000000;
        std::cout << "Broadcasting num_steps: " << num_steps << std::endl;
    }

    // 2. 广播 (Broadcast): Rank 0 把 num_steps 发送给所有人
    // 所有进程都必须调用这个函数
    MPI_Bcast(&num_steps, 1, MPI_LONG, 0, MPI_COMM_WORLD);

    // 3. 并行计算：每个进程负责一部分循环
    double step = 1.0 / (double)num_steps;
    double local_sum = 0.0;
    
    // 这种步长切分方式（Round-Robin）其实不太好，更好的方式是块状切分
    // 但为了代码简单，我们让每个进程处理 i, i+size, i+2*size...
    for (long i = world_rank; i < num_steps; i += world_size) {
        double x = (i + 0.5) * step;
        local_sum += 4.0 / (1.0 + x * x);
    }
    double local_pi_part = local_sum * step;

    // 4. 归约 (Reduce): 将所有进程的 local_pi_part 加起来，结果存到 Rank 0 的 global_pi
    double global_pi = 0.0;
    MPI_Reduce(&local_pi_part, &global_pi, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    // 5. 只有 Rank 0 打印结果
    if (world_rank == 0) {
        std::cout << "Calculated PI: " << global_pi << std::endl;
        std::cout << "Error: " << std::abs(global_pi - 3.141592653589793) << std::endl;
    }

    MPI_Finalize();
    return 0;
}
