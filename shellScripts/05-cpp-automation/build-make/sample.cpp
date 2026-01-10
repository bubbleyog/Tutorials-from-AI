// 示例C++程序：用于Shell脚本自动化演示
//
// 特点：
// - 支持命令行参数：--name/--sleep/--seed/--fail
// - 输出一行结构化结果（TAB分隔的 key=value），便于Shell提取
// - 可通过 --fail 演示失败退出码
//
// 编译示例：
//   g++ -std=c++17 -O2 -Wall -Wextra -o sample_app sample.cpp
//
// 运行示例：
//   ./sample_app --name Alice --seed 1

#include <chrono>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>

struct Args {
    std::string name = "world";
    double sleep_sec = 0.0;
    int seed = 0;
    bool fail = false;
};

static void print_usage(const char* prog) {
    std::cerr << "Usage: " << prog << " [--name NAME] [--sleep SEC] [--seed N] [--fail]\n";
}

static bool parse_args(int argc, char** argv, Args& out) {
    for (int i = 1; i < argc; i++) {
        const char* a = argv[i];

        if (std::strcmp(a, "--name") == 0) {
            if (i + 1 >= argc) return false;
            out.name = argv[++i];
        } else if (std::strcmp(a, "--sleep") == 0) {
            if (i + 1 >= argc) return false;
            out.sleep_sec = std::stod(argv[++i]);
        } else if (std::strcmp(a, "--seed") == 0) {
            if (i + 1 >= argc) return false;
            out.seed = std::stoi(argv[++i]);
        } else if (std::strcmp(a, "--fail") == 0) {
            out.fail = true;
        } else if (std::strcmp(a, "-h") == 0 || std::strcmp(a, "--help") == 0) {
            print_usage(argv[0]);
            std::exit(0);
        } else {
            return false;
        }
    }
    return true;
}

static std::string now_iso_local() {
    using clock = std::chrono::system_clock;
    const auto now = clock::now();
    const auto t = clock::to_time_t(now);

    std::tm tm{};
#ifdef _WIN32
    localtime_s(&tm, &t);
#else
    localtime_r(&t, &tm);
#endif

    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%dT%H:%M:%S");
    return oss.str();
}

int main(int argc, char** argv) {
    Args args;
    if (!parse_args(argc, argv, args)) {
        print_usage(argv[0]);
        std::cerr << "ERROR: invalid arguments\n";
        return 64;  // EX_USAGE
    }

    if (args.sleep_sec > 0) {
        std::this_thread::sleep_for(std::chrono::duration<double>(args.sleep_sec));
    }

    if (args.fail) {
        std::cerr << "[" << now_iso_local() << "] ERROR: simulated failure\n";
        return 2;
    }

    std::mt19937 rng(static_cast<std::mt19937::result_type>(args.seed));
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    const double metric = dist(rng);

    // 输出：单行、TAB分隔，便于Shell解析
    std::cout << "time=" << now_iso_local() << "\t"
              << "name=" << args.name << "\t"
              << "seed=" << args.seed << "\t"
              << "metric=" << std::fixed << std::setprecision(6) << metric << "\n";

    return 0;
}
