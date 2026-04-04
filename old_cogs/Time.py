import time
from datetime import datetime, timezone
import dateparser
import discord
from discord.ext import commands

class Time(commands.Cog):
    """⏰ Time-related commands with timezone support and natural language parsing."""
    
    def __init__(self, client):
        self.client = client

    async def parse_time_input(self, input_str):
        """Parse natural language time input into a Unix timestamp."""
        parsed = dateparser.parse(input_str, settings={'TO_TIMEZONE': 'UTC'})
        return int(parsed.timestamp()) if parsed else None

    @commands.command(
        name="time",
        usage="[time/date]",
        help="""
        Get the current time or convert a time/date to Discord's timestamp format.
        Supports natural language (e.g., "in 2 hours", "next Friday 3pm EST").
        """
    )
    async def time(self, ctx, *, message=None):
        """
        Examples:
        - `!time` → Shows current time
        - `!time in 3 hours` → Shows time 3 hours from now
        - `!time December 25 2025 14:30 EST` → Converts to timestamp
        """
        if not message:
            t = int(time.time())
            await ctx.send(f"⏰ **Current time:** <t:{t}:T> (`<t:{t}:R>`)")
            return

        t = await self.parse_time_input(message)
        if not t:
            await ctx.send(
                "❌ **Invalid time format!** Try:\n"
                "- `now`, `tomorrow 8am`, `in 2 hours`\n"
                "- `2025-12-25 14:30`, `14:30` (today)\n"
                "- Add a timezone like `EST`, `PST`, or `UTC`"
            )
            return

        embed = discord.Embed(
            title="⏰ Time Conversion",
            description=(
                f"**Your input:** `{message}`\n"
                f"**Converted to:** <t:{t}:F> (`<t:{t}:R>`)"
            ),
            color=discord.Color.blue()
        )
        embed.add_field(name="Unix Timestamp", value=f"`{t}`")
        await ctx.send(embed=embed)

    @commands.command(
        name="countdown",
        usage="<time/date>",
        help="""
        Shows a countdown to a specific time/date.
        Supports natural language (e.g., "in 30 minutes", "next New Year's").
        """
    )
    async def countdown(self, ctx, *, message):
        """
        Examples:
        - `.countdown December 25` → Days until Christmas
        - `.countdown in 1 hour` → Countdown to 1 hour from now
        - `.countdown 2026-01-01 00:00 UTC` → New Year's countdown
        """
        parsed_time = dateparser.parse(message)
        if not parsed_time:
            await ctx.send(
                "❌ **Invalid time format!** Try:\n"
                "- `in 10 minutes`, `tomorrow 9am`\n"
                "- `2025-12-25`, `14:30` (today)\n"
                "- Add a timezone like `UTC` or `PST`"
            )
            return

        now = datetime.now(timezone.utc)
        delta = parsed_time - now

        if delta.total_seconds() <= 0:
            await ctx.send("⏰ **That time has already passed!**")
            return

        embed = discord.Embed(
            title="⏳ Countdown",
            description=(
                f"**Target:** <t:{int(parsed_time.timestamp())}:F>\n"
                f"**Time remaining:** `{delta.days}` days, `{delta.seconds//3600}` hours, `{(delta.seconds//60)%60}` minutes"
            ),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Time(client))
