import aiohttp
import asyncio
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("hypixel_punishment_stats", "Xiaoxin", "查询Hypixel封禁统计数据", "1.0.0")
class HypixelPunishmentStatsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "https://api.plancke.io/hypixel/v1/punishmentStats"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://plancke.io/",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Connection": "keep-alive",
        }
        self.cookies = {}

    async def initialize(self):
        logger.info("Hypixel封禁统计插件已加载（命令：/hacker）")

    async def fetch_ban_stats(self):
        """获取封禁统计数据，返回 (success, data_dict or error_msg)"""
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout, cookies=self.cookies) as session:
                async with session.get(self.api_url, headers=self.headers, ssl=False) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("success"):
                            record = data.get("record", {})
                            return True, {
                                "watchdog_total": record.get("watchdog_total", 0),
                                "staff_total": record.get("staff_total", 0),
                                "watchdog_daily": record.get("watchdog_rollingDaily", 0),
                                "staff_daily": record.get("staff_rollingDaily", 0),
                                "watchdog_last_minute": record.get("watchdog_lastMinute", 0)
                            }
                        else:
                            return False, "API 返回失败状态"
                    else:
                        return False, f"HTTP {resp.status}"
        except asyncio.TimeoutError:
            return False, "请求超时"
        except aiohttp.ClientError as e:
            return False, f"网络错误: {e}"
        except Exception as e:
            return False, f"未知错误: {e}"

    def format_stats(self, stats):
        def fmt(num):
            return f"{num:,}"
        return (
            f"📊 **Hypixel 封禁统计**\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"🤡 **Watchdog 封禁**\n"
            f"   • 总计：{fmt(stats['watchdog_total'])}\n"
            f"   • 过去24小时：{fmt(stats['watchdog_daily'])}\n"
            f"   • 过去1分钟：{fmt(stats['watchdog_last_minute'])}\n"
            f"\n"
            f"🚨 **Staff 手动封禁**\n"
            f"   • 总计：{fmt(stats['staff_total'])}\n"
            f"   • 过去24小时：{fmt(stats['staff_daily'])}\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Dev：XiaoXin1336"
        )

    @filter.command("hacker")
    async def hacker(self, event: AstrMessageEvent):
        """查询Hypixel封禁统计，用法：/hacker"""
        yield event.plain_result("正在查询封禁统计信息，请稍候...")
        success, result = await self.fetch_ban_stats()
        if success:
            reply = self.format_stats(result)
            yield event.plain_result(reply)
        else:
            yield event.plain_result(f"❌ 获取数据失败：{result}")

    async def terminate(self):
        logger.info("Hypixel封禁统计插件已卸载")