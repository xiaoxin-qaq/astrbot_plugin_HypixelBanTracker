Hypixel 封禁统计插件

安装方法

1. 将 hypixel_punishment_stats.py 放入 AstrBot 的插件目录（addons/ 或 plugins/）。
2. 重启 AstrBot 或执行热加载。
3. 确保已安装依赖 aiohttp（通常已自带）。

输出格式

发送 /hacker 命令后，机器人回复示例：

📊 Hypixel 封禁统计
━━━━━━━━━━━━━━━━━
🤡 Watchdog 封禁
   • 总计：10,254,905
   • 过去24小时：880
   • 过去1分钟：0

🚨 Staff 手动封禁
   • 总计：5,593,892
   • 过去24小时：2,058
━━━━━━━━━━━━━━━━━
数据来源：Hypixel Public API

数字自动添加千位分隔符。

更新日志

v1.3.0 (2026-06-13)
- 统一触发命令为 /hacker
- 移除定时播报功能，仅保留单次查询
- 增加完整浏览器请求头
- 支持配置 Cookie 绕过 Cloudflare

v1.2.0 (2026-06-13)
- 移除定时任务，简化为纯查询插件

v1.0.0 (2026-06-12)
- 初始版本，支持 /hbt 命令

作者

YourName
MIT License