# HPC 服务使用教程设计文档 (v2.0)

## 1. 项目概述
本教程旨在为用户提供全面、清晰的高性能计算（HPC）服务使用指南。教程将涵盖 Linux 基础操作、专门针对 HPC 环境的系统操作，以及两大主流调度系统（PBS 和 Slurm）的详细使用说明。目标受众包括 HPC 新手和有一定经验的研究人员。

**更新重点**：采用模块化目录结构，每个章节独立成文件夹，包含教程文本、可运行的示例代码以及对示例程序的详细解释（独立文档或内嵌）。

## 2. 文件目录结构设计
```text
tutorials/HPC_Using/
├── 00_Design/
│   └── HPC_Tutorial_Design_Document.md    # 本设计文档
├── 01_Linux_Basics_and_Environment/       # 第一部分：Linux 基础与 HPC 环境
│   ├── Tutorial_Content.md                # 核心教程：命令行、文件管理、模块系统
│   ├── Example_Code_Explanations.md       # 对示例代码的逐行/逐块解释
│   └── examples/                          # 可运行示例脚本库
│       ├── 01_hello.sh                    # 基础 Shell 脚本示例
│       ├── 02_env_vars.sh                 # 环境变量操作示例
│       └── 03_module_demo.sh              # module 命令模拟流程
├── 02_PBS_Scheduler_Guide/                # 第二部分：PBS 调度系统
│   ├── Tutorial_Content.md                # 核心教程：PBS 原理、qsub/qstat 命令
│   ├── Example_Code_Explanations.md       # 作业脚本的详细参数解读
│   └── examples/                          # PBS 作业脚本模板
│       ├── 01_basic_job.pbs               # 基础单节点作业
│       ├── 02_mpi_job.pbs                 # MPI 并行作业
│       ├── 03_openmp_job.pbs              # OpenMP 多线程作业
│       ├── 04_gpu_job.pbs                 # GPU 资源申请作业
│       └── 05_interactive.sh              # 交互式作业启动命令示例
├── 03_Slurm_Scheduler_Guide/              # 第三部分：Slurm 调度系统
│   ├── Tutorial_Content.md                # 核心教程：Slurm 架构、sbatch/squeue 命令
│   ├── Example_Code_Explanations.md       # 主要参数与 srun 机制解读
│   └── examples/                          # Slurm 作业脚本模板
│       ├── 01_basic_job.slurm             # 基础相关
│       ├── 02_mpi_job.slurm               # MPI (srun)
│       ├── 03_openmp_job.slurm            # OpenMP
│       ├── 04_gpu_job.slurm               # GPU
│       └── 05_array_job.slurm             # 数组作业示例
└── 04_Appendix/                           # 第四部分：附录
    ├── PBS_Slurm_Rosetta_Stone.md         # 命令对照速查表
    └── Common_Errors_and_FAQ.md           # 常见错误与解答
```

## 3. 详细内容规划

### 第一部分：Linux 基础与 HPC 环境 (01_Linux_Basics_and_Environment)
*   **教程内容 (`Tutorial_Content.md`)**:
    *   SSH 登录技巧 (配置 `.ssh/config`)。
    *   核心命令 (文件操作、权限、文本处理)。
    *   HPC 核心概念：登录节点 vs 计算节点。
    *   Environment Modules (`module load/avail/list`)。
*   **示例代码 (`examples/`)**:
    *   `hello.sh`: 展示 Shebang、打印输出、简单变量。
    *   `env_vars.sh`: 展示 PATH, LD_LIBRARY_PATH 的查看与临时修改。
    *   `module_demo.sh`: 演示模块加载前后的环境变化。
*   **代码解释 (`Example_Code_Explanations.md`)**:
    *   解释 Shell 脚本的基本语法结构（变量、循环、条件判断）。
    *   详细说明环境变量如何作为程序运行的“上下文”。

### 第二部分：PBS 调度系统实战 (02_PBS_Scheduler_Guide)
*   **教程内容 (`Tutorial_Content.md`)**:
    *   PBS 工作流与队列概念。
    *   `qsub` 指令详解 (`-l`, `-q`, `-N` 等)。
    *   作业管理 (`qstat`, `qdel`, `qalter`)。
*   **示例代码 (`examples/`)**:
    *   `basic_job.pbs`: 标准模板，包含最常用的 header 指令。
    *   `mpi_job.pbs`: 展示如何配合 mpirun/mpiexec 使用，以及如何获取节点列表。
    *   `gpu_job.pbs`: 展示 GPU 队列与资源申请语法。
*   **代码解释 (`Example_Code_Explanations.md`)**:
    *   逐行拆解 `#PBS` 指令的含义。
    *   解释 MPI 运行环境的加载过程。

### 第三部分：Slurm 调度系统实战 (03_Slurm_Scheduler_Guide)
*   **教程内容 (`Tutorial_Content.md`)**:
    *   Slurm 架构与分区 (Partition/QOS)。
    *   `sbatch` 指令详解 (`--nodes`, `--ntasks`, `--gres` 等)。
    *   作业查询与控制 (`squeue`, `scancel`, `sacct`)。
*   **示例代码 (`examples/`)**:
    *   `basic_job.slurm`: 标准 Slurm 脚本模板。
    *   `mpi_job.slurm`: 展示 `srun` 的关键作用。
    *   `array_job.slurm`: 批量处理大量文件的示例。
*   **代码解释 (`Example_Code_Explanations.md`)**:
    *   对比 `#SBATCH` 与 `#PBS` 的异同。
    *   深入解释 `ntasks` vs `cpus-per-task`。

### 第四部分：附录 (04_Appendix)
*   `PBS_Slurm_Rosetta_Stone.md`: 左右对照表，方便迁移用户查阅。
*   `Common_Errors_and_FAQ.md`: 常见问题，如 "Job stuck in queue", "Memory limit exceeded" 等。

## 4. 编写规范
1.  **独立性**: 每个目录下的内容应尽可能自包含，用户下载一个目录即可学习对应模块。
2.  **实战导向**: 所有解释必须配合 `examples/` 文件夹中的脚本进行引用（如 "参见 `examples/01_basic_job.slurm` 第 5 行..."）。
3.  **清晰注释**: 示例代码中的每一行重要指令都需包含注释。

