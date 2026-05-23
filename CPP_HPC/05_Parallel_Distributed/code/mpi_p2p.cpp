#include <mpi.h>
#include <iostream>

// MPI Ping-Pong
// 演示点对点通信 (Point-to-Point Communication)
// Rank 0 发送给 Rank 1，Rank 1 接收后再发回给 Rank 0

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // 至少需要 2 个进程
    if (world_size < 2) {
        if (world_rank == 0) {
            std::cerr << "World size must be greater than 1 for ping pong" << std::endl;
        }
        MPI_Finalize();
        return 0;
    }

    const int PING_PONG_LIMIT = 10;
    int ping_pong_count = 0;
    int partner_rank = (world_rank + 1) % 2; // 0 <-> 1

    // 只让 Rank 0 和 Rank 1 参与
    if (world_rank < 2) {
        while (ping_pong_count < PING_PONG_LIMIT) {
            if (world_rank == ping_pong_count % 2) {
                // 当前轮次由我发送
                ping_pong_count++;
                MPI_Send(&ping_pong_count, 1, MPI_INT, partner_rank, 0, MPI_COMM_WORLD);
                printf("%d sent and incremented ping_pong_count %d to %d\n",
                       world_rank, ping_pong_count, partner_rank);
            } else {
                // 当前轮次由我接收
                MPI_Recv(&ping_pong_count, 1, MPI_INT, partner_rank, 0, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
                printf("%d received ping_pong_count %d from %d\n",
                       world_rank, ping_pong_count, partner_rank);
            }
        }
    }

    MPI_Finalize();
    return 0;
}
