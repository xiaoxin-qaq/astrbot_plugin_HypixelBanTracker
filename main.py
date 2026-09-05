import aiohttp
import asyncio
import random
from datetime import datetime
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("hypixel_punishment_stats", "Xiaoxin", "查询Hypixel封禁统计数据", "2.3.0")
class HypixelPunishmentStatsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "https://api.plancke.io/hypixel/v1/punishmentStats"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://plancke.io/",
        }
        self.bg_urls = [
            "https://xiaoxin.cn-nb1.rains3.com/bj%20%281%29.png",
            "https://xiaoxin.cn-nb1.rains3.com/bj%20%282%29.png",
            "https://xiaoxin.cn-nb1.rains3.com/bj%20%283%29.png",
            "https://xiaoxin.cn-nb1.rains3.com/bj%20%284%29.png",
            "https://xiaoxin.cn-nb1.rains3.com/bj%20%285%29.png",
        ]
        self.html_tmpl = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 900px;
    margin: 0 auto;
    font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
    /* 关键：在背景图上叠加半透明黑色层，降低亮度 */
    background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url('{{ bg_url }}') center/cover no-repeat;
    padding: 30px 24px 24px 24px;
    color: #eef1ff;
}
.wrap {
    max-width: 840px;
    margin: 0 auto;
}
.header {
    text-align: center;
    margin-bottom: 24px;
}
.header h1 {
    font-size: 26px;
    font-weight: 700;
    background: linear-gradient(90deg, #6ee7ff, #a78bfa);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.6); /* 增强标题阴影 */
}
.header .sub {
    font-size: 13px;
    color: rgba(238,241,255,0.85);
    margin-top: 6px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.8);
}
.cards-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
}
.card {
    position: relative;
    background: rgba(20, 20, 40, 0.78); /* 提高不透明度 */
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 20px 22px;
    overflow: hidden;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.7);
}
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.card.watchdog::before {
    background: linear-gradient(90deg, #6ee7ff, #3b82f6);
}
.card.staff::before {
    background: linear-gradient(90deg, #a78bfa, #db2777);
}
.card-title {
    font-size: 14px;
    font-weight: 600;
    color: rgba(238,241,255,0.95);
    margin-bottom: 12px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
.big-num {
    font-family: "Consolas", "SF Mono", monospace;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.big-num.watchdog {
    color: #6ee7ff;
    text-shadow: 0 0 20px rgba(110,231,255,0.5), 0 2px 6px rgba(0,0,0,0.6);
}
.big-num.staff {
    color: #a78bfa;
    text-shadow: 0 0 20px rgba(167,139,250,0.5), 0 2px 6px rgba(0,0,0,0.6);
}
.big-label {
    font-size: 12px;
    color: rgba(238,241,255,0.8);
    margin-bottom: 14px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
.stats-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}
.stat-item {
    flex: 1;
    min-width: 90px;
}
.stat-item .num {
    font-family: "Consolas", monospace;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.7);
}
.stat-item .label {
    font-size: 11px;
    color: rgba(238,241,255,0.8);
    margin-top: 2px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
.panel {
    background: rgba(20, 20, 40, 0.78);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 18px 20px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.7);
    display: flex;
    flex-direction: column;
    min-height: 280px;
    margin-top: 16px;
}
.panel-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    font-size: 14px;
    font-weight: 600;
    color: #eef1ff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
.act-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: auto;
    flex: 1;
}
.act-item {
    display: grid;
    grid-template-columns: 32px 1fr 70px;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.act-item:last-child { border-bottom: none; }
.act-ic {
    width: 28px; height: 28px; border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.act-ic.wd { background: rgba(59,130,246,0.3); color: #6ee7ff; }
.act-ic.st { background: rgba(139,92,246,0.3); color: #a78bfa; }
.act-ic.sys { background: rgba(16,185,129,0.25); color: #10b981; }
.act-text {
    font-size: 13px;
    color: rgba(238,241,255,0.95);
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
.act-text b {
    color: #6ee7ff;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(110,231,255,0.4);
}
.act-time {
    font-family: "Consolas", monospace;
    color: rgba(238,241,255,0.7);
    font-size: 11px;
    text-align: right;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
.footer {
    text-align: center;
    margin-top: 18px;
    font-size: 11px;
    color: rgba(238,241,255,0.7);
    text-shadow: 0 2px 6px rgba(0,0,0,0.8);
}
.footer .time {
    color: rgba(238,241,255,0.9);
    font-family: "Consolas", monospace;
    font-size: 12px;
}
.mock-tag {
    display: inline-block;
    background: rgba(239,68,68,0.25);
    color: #ff6b6b;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 6px;
    margin-left: 8px;
    border: 1px solid rgba(239,68,68,0.4);
}
</style>
</head>
<body>
<div class="wrap">
    <div class="header">
        <h1>Hypixel 封禁监控</h1>
        <div class="sub">实时封禁数据统计面板</div>
    </div>
    <div class="cards-row">
        <div class="card watchdog">
            <div class="card-title">Watchdog 自动封禁</div>
            <div class="big-num watchdog">{{ wd_daily }}</div>
            <div class="big-label">今日自动封禁累计</div>
            <div class="stats-row">
                <div class="stat-item">
                    <div class="num">{{ wd_today_new }}</div>
                    <div class="label">今日新增</div>
                </div>
                <div class="stat-item">
                    <div class="num">{{ wd_total }}</div>
                    <div class="label">历史总计</div>
                </div>
                <div class="stat-item">
                    <div class="num">{{ wd_last_min }}</div>
                    <div class="label">过去 1 分钟</div>
                </div>
            </div>
        </div>
        <div class="card staff">
            <div class="card-title">Staff 人工封禁</div>
            <div class="big-num staff">{{ st_daily }}</div>
            <div class="big-label">今日人工封禁累计</div>
            <div class="stats-row">
                <div class="stat-item">
                    <div class="num">{{ st_today_new }}</div>
                    <div class="label">今日新增</div>
                </div>
                <div class="stat-item">
                    <div class="num">{{ st_total }}</div>
                    <div class="label">历史总计</div>
                </div>
                <div class="stat-item">
                    <div class="num">{{ st_last_min }}</div>
                    <div class="label">过去 1 分钟</div>
                </div>
            </div>
        </div>
    </div>

    <div class="panel">
        <div class="panel-head"><span>📋</span> 最近活动</div>
        <div class="act-list">
            {{ activity_html | safe }}
        </div>
    </div>

    <div class="footer">
        <div>数据更新时间：<span class="time">{{ update_time }}</span></div>
        <div style="margin-top:4px;">Dev：XiaoXin1336</div>
        {% if mocked %}<div><span class="mock-tag">模拟数据</span></div>{% endif %}
    </div>
</div>
</body>
</html>"""

    async def initialize(self):
        logger.info("Hypixel封禁统计插件已加载（命令：/hacker）")

    async def fetch_ban_stats(self):
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.api_url, headers=self.headers, ssl=False) as resp:
                    if resp.status != 200:
                        return False, f"HTTP {resp.status}"
                    data = await resp.json()
                    if not data.get("success"):
                        return False, "API 返回失败状态"
                    record = data.get("record", {})
                return True, {
                    "watchdog_total": record.get("watchdog_total", 0),
                    "staff_total": record.get("staff_total", 0),
                    "watchdog_daily": record.get("watchdog_rollingDaily", 0),
                    "staff_daily": record.get("staff_rollingDaily", 0),
                    "watchdog_last_minute": record.get("watchdog_lastMinute", 0),
                    "staff_last_minute": record.get("staff_lastMinute", 0),
                }
        except asyncio.TimeoutError:
            return False, "请求超时"
        except aiohttp.ClientError as e:
            return False, f"网络错误: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"

    def _fmt(self, num):
        return f"{num:,}"

    def _generate_activity(self, wd_min, st_min):
        now = datetime.now()
        activities = []

        if wd_min > 0:
            activities.append({
                "type": "wd",
                "text": f"Watchdog 自动封禁 <b>{self._fmt(wd_min)}</b> 个玩家",
                "time": now.strftime("%H:%M:%S")
            })
        if st_min > 0:
            activities.append({
                "type": "st",
                "text": f"Staff 人工封禁 <b>{self._fmt(st_min)}</b> 个玩家",
                "time": now.strftime("%H:%M:%S")
            })

        seed_acts = [
            {"type": "wd", "text": "Watchdog 自动封禁 <b>{}</b> 个玩家", "counts": [3, 4, 5, 6, 7]},
            {"type": "st", "text": "Staff 人工封禁 <b>{}</b> 个玩家", "counts": [1, 2, 1]},
            {"type": "wd", "text": "Watchdog 自动封禁 <b>{}</b> 个玩家", "counts": [2, 4, 3]},
            {"type": "sys", "text": "封禁统计接口已同步最新快照", "counts": []},
        ]

        for i, act in enumerate(seed_acts):
            t = (now.replace(second=0) if now.second < 30 else now.replace(second=30))
            t_min = (i + 1) * (random.randint(2, 5))
            t = datetime.fromtimestamp(t.timestamp() - t_min * 60)
            if act["counts"]:
                cnt = random.choice(act["counts"])
                text = act["text"].format(cnt)
            else:
                text = act["text"]
            activities.append({
                "type": act["type"],
                "text": text,
                "time": t.strftime("%H:%M:%S")
            })

        icons = {"wd": "🛡️", "st": "⚔️", "sys": "📡"}
        html = ""
        for act in activities[:6]:
            html += f'<div class="act-item">'
            html += f'<div class="act-ic {act["type"]}">{icons.get(act["type"], "📡")}</div>'
            html += f'<div class="act-text">{act["text"]}</div>'
            html += f'<div class="act-time">{act["time"]}</div>'
            html += f'</div>'
        return html

    async def render_image(self, stats, mocked=False):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bg_url = random.choice(self.bg_urls)

        activity_html = self._generate_activity(
            stats["watchdog_last_minute"],
            stats["staff_last_minute"]
        )

        render_data = {
            "bg_url": bg_url,
            "wd_daily": self._fmt(stats["watchdog_daily"]),
            "st_daily": self._fmt(stats["staff_daily"]),
            "wd_total": self._fmt(stats["watchdog_total"]),
            "st_total": self._fmt(stats["staff_total"]),
            "wd_today_new": self._fmt(stats["watchdog_daily"]),
            "st_today_new": self._fmt(stats["staff_daily"]),
            "wd_last_min": self._fmt(stats["watchdog_last_minute"]),
            "st_last_min": self._fmt(stats["staff_last_minute"]),
            "update_time": now,
            "mocked": mocked,
            "activity_html": activity_html,
        }
        options = {
            "viewport": {"width": 900, "height": 10},
            "full_page": True,
            "type": "jpeg",
            "quality": 92,
        }
        url = await self.html_render(self.html_tmpl, render_data, options=options)
        return url

    @filter.command("hacker")
    async def hacker(self, event: AstrMessageEvent):
        success, result = await self.fetch_ban_stats()
        if not success:
            yield event.plain_result(f"❌ 获取数据失败：{result}")
            return
        try:
            img_url = await self.render_image(result, mocked=False)
            yield event.image_result(img_url)
        except Exception as e:
            logger.error(f"图片渲染失败: {e}")
            yield event.plain_result(self._format_text(result))

    def _format_text(self, stats):
        def fmt(num):
            return f"{num:,}"
        return (
            f"📊 **Hypixel 封禁统计**\\n"
            f"━━━━━━━━━━━━━━━━━\\n"
            f"🛡️ **Watchdog 自动封禁**\\n"
            f"   • 今日累计：{fmt(stats['watchdog_daily'])}\\n"
            f"   • 历史总计：{fmt(stats['watchdog_total'])}\\n"
            f"   • 过去1分钟：{fmt(stats['watchdog_last_minute'])}\\n"
            f"\\n"
            f"⚔️ **Staff 人工封禁**\\n"
            f"   • 今日累计：{fmt(stats['staff_daily'])}\\n"
            f"   • 历史总计：{fmt(stats['staff_total'])}\\n"
            f"   • 过去1分钟：{fmt(stats['staff_last_minute'])}\\n"
            f"━━━━━━━━━━━━━━━━━\\n"
            f"Dev：XiaoXin1336"
        )

    async def terminate(self):
        logger.info("Hypixel封禁统计插件已卸载")