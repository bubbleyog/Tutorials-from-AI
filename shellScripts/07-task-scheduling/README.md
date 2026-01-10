# 第7章：本地任务调度

> 本章介绍Linux本地定时/一次性任务的三种常见方式：cron、at、systemd timer，并给出脚本化的模板与注意事项。

## 📋 本章概述

在服务器上，常见的“定时跑任务”场景包括：

- 每天定时拉取数据、清理临时文件、压缩日志
- 每隔N分钟跑一次监控/健康检查
- 只执行一次的延迟任务（比如“1小时后重启某服务”）

本章强调两点：

- **可复现**：用脚本生成配置/单位文件，避免手工操作遗漏
- **可观察**：明确日志位置与退出码，方便排查

## 🎯 学习目标

完成本章学习后，你将能够：

- 编写cron任务并理解cron环境差异（PATH、工作目录、SHELL）
- 使用at提交一次性任务，并查看/取消队列
- 使用systemd timer（尤其是用户级timer）管理周期任务

---

## 7.1 cron（周期任务）

适合：固定周期、稳定长期运行的任务。

📄 **示例脚本**: [01-cron-basics.sh](01-cron-basics.sh)

### cron语法速查

```
# ┌──────── 分钟(0-59)
# │ ┌────── 小时(0-23)
# │ │ ┌──── 月日(1-31)
# │ │ │ ┌── 月份(1-12)
# │ │ │ │ ┌─ 星期(0-7, 0/7=周日)
# │ │ │ │ │
# * * * * *  command
```

> ⚠️ 注意：cron默认环境非常“瘦”。务必使用**绝对路径**，并显式设置 `PATH`/`SHELL`。

---

## 7.2 at（一次性任务）

适合：只执行一次的延迟任务。

📄 **示例脚本**: [02-at-command.sh](02-at-command.sh)

---

## 7.3 systemd timer（现代定时器）

适合：需要更强可控性/可观察性的周期任务（日志、依赖、重启策略）。

📄 **示例脚本**: [03-systemd-timer.sh](03-systemd-timer.sh)

> 💡 建议优先使用用户级timer（`systemctl --user`）做个人任务，不需要root权限。

---

## 🧾 快速参考

| 需求 | 推荐方式 | 常用命令 |
|------|----------|----------|
| 每5分钟跑一次 | cron/systemd timer | `crontab -e` / `systemctl --user enable --now *.timer` |
| 每天凌晨跑一次 | cron/systemd timer | `0 0 * * * ...` / `OnCalendar=daily` |
| 10分钟后执行一次 | at | `echo "cmd" | at now + 10 minutes` |
| 查看任务 | cron/at/systemd | `crontab -l` / `atq` / `systemctl --user list-timers` |
| 取消任务 | cron/at/systemd | `crontab -e` / `atrm <id>` / `systemctl --user disable --now *.timer` |
