#!/usr/bin/env python3
"""示例Python程序：用于Shell脚本自动化演示。

特点：
- 支持命令行参数（--name/--sleep/--seed/--fail）
- 支持环境变量（APP_MODE/APP_RUN_ID）
- 输出一行结构化结果，便于脚本收集

用法示例：
  python3 sample.py --name Alice --seed 1
  APP_MODE=prod APP_RUN_ID=run001 python3 sample.py --sleep 0.2
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from datetime import datetime, timezone


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shell自动化示例程序")
    parser.add_argument("--name", default="world", help="用于演示的名字")
    parser.add_argument("--sleep", type=float, default=0.0, help="模拟耗时（秒）")
    parser.add_argument("--seed", type=int, default=0, help="随机种子（用于批量扫描）")
    parser.add_argument(
        "--fail",
        action="store_true",
        help="演示失败：若指定则以退出码2退出",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    app_mode = os.environ.get("APP_MODE", "dev")
    run_id = os.environ.get("APP_RUN_ID", "")

    # 输出一些基本信息
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    python_bin = sys.executable

    random.seed(args.seed)
    metric = random.random()

    if args.sleep > 0:
        time.sleep(args.sleep)

    if args.fail:
        # 让stdout/stderr都能看到一些内容
        print(f"[{now}] ERROR: simulated failure", file=sys.stderr)
        return 2

    # 结构化输出（单行），便于Shell用awk/cut等处理
    # 字段以TAB分隔，避免名字中空格导致解析困难
    fields = {
        "time": now,
        "name": args.name,
        "mode": app_mode,
        "run_id": run_id,
        "seed": str(args.seed),
        "metric": f"{metric:.6f}",
        "python": python_bin,
    }

    print(
        "\t".join(
            [
                f"time={fields['time']}",
                f"name={fields['name']}",
                f"mode={fields['mode']}",
                f"run_id={fields['run_id']}",
                f"seed={fields['seed']}",
                f"metric={fields['metric']}",
                f"python={fields['python']}",
            ]
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
