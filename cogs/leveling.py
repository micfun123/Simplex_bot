import discord
from discord.ext import commands
from discord import option
import aiosqlite
import httpx
import random
import logging
import asyncio
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Setup logging
logger = logging.getLogger("simplex.leveling")

class Leveling(commands.Cog):
    """Native leveling system with custom XP logic and rank cards."""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/leveling.db"
        self.cooldowns = {} # (guild_id, user_id): last_xp_time
        self.settings_cache = {} # guild_id: {enabled: bool, wipe: bool, ignored: set}
        
    def get_xp_for_level(self, level: int) -> int:
        """Formula: 5 * (level**2) + (50 * level) + 100"""
        return 5 * (level**2) + (50 * level) + 100

    async def get_guild_settings(self, guild_id: int):
        if guild_id in self.settings_cache:
            return self.settings_cache[guild_id]
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT enabled, wipe_on_leave FROM guild_config WHERE guild_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    await db.execute("INSERT OR IGNORE INTO guild_config (guild_id) VALUES (?)", (guild_id,))
                    await db.commit()
                    enabled, wipe = 1, 0
                else:
                    enabled, wipe = row
            
            async with db.execute("SELECT channel_id FROM ignored_channels WHERE guild_id = ?", (guild_id,)) as cursor:
                ignored = {r[0] for r in await cursor.fetchall()}
        
        settings = {"enabled": bool(enabled), "wipe": bool(wipe), "ignored": ignored}
        self.settings_cache[guild_id] = settings
        return settings

    def clear_cache(self, guild_id: int):
        if guild_id in self.settings_cache:
            del self.settings_cache[guild_id]

    # Slash Command Group
    leveling = discord.SlashCommandGroup("leveling", "Leveling system management")

    @leveling.command(name="toggle", description="Enable or disable leveling on this server")
    @commands.has_permissions(administrator=True)
    async def toggle_leveling(self, ctx):
        settings = await self.get_guild_settings(ctx.guild.id)
        new_status = 0 if settings["enabled"] else 1
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE guild_config SET enabled = ? WHERE guild_id = ?", (new_status, ctx.guild.id))
            await db.commit()
        self.clear_cache(ctx.guild.id)
        await ctx.respond(f"✅ Leveling has been **{'enabled' if new_status else 'disabled'}**.")

    @leveling.command(name="wipe_toggle", description="Toggle XP wipe when members leave")
    @commands.has_permissions(administrator=True)
    async def toggle_wipe(self, ctx):
        settings = await self.get_guild_settings(ctx.guild.id)
        new_status = 0 if settings["wipe"] else 1
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE guild_config SET wipe_on_leave = ? WHERE guild_id = ?", (new_status, ctx.guild.id))
            await db.commit()
        self.clear_cache(ctx.guild.id)
        await ctx.respond(f"✅ XP wipe on leave is now **{'enabled' if new_status else 'disabled'}**.")

    @leveling.command(name="ignore_channel", description="Disable XP in a channel")
    @commands.has_permissions(administrator=True)
    async def ignore_channel(self, ctx, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR IGNORE INTO ignored_channels (guild_id, channel_id) VALUES (?, ?)", (ctx.guild.id, channel.id))
            await db.commit()
        self.clear_cache(ctx.guild.id)
        await ctx.respond(f"✅ XP disabled in {channel.mention}.")

    @leveling.command(name="unignore_channel", description="Enable XP in a channel")
    @commands.has_permissions(administrator=True)
    async def unignore_channel(self, ctx, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM ignored_channels WHERE guild_id = ? AND channel_id = ?", (ctx.guild.id, channel.id))
            await db.commit()
        self.clear_cache(ctx.guild.id)
        await ctx.respond(f"✅ XP enabled in {channel.mention}.")

    async def award_xp(self, member, amount, bypass_cooldown=False):
        if member.bot: return False
        
        guild_id, user_id = member.guild.id, member.id
        if not bypass_cooldown:
            now = datetime.now().timestamp()
            if now - self.cooldowns.get((guild_id, user_id), 0) < 60: return False
            self.cooldowns[(guild_id, user_id)] = now

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT xp, level, total_xp FROM user_levels WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                row = await cursor.fetchone()
                xp, level, total_xp = (row[0] + amount, row[1], row[2] + amount) if row else (amount, 0, amount)
            
            leveled_up = False
            while xp >= self.get_xp_for_level(level):
                xp -= self.get_xp_for_level(level)
                level += 1
                leveled_up = True
            
            await db.execute("""
                INSERT INTO user_levels (guild_id, user_id, xp, level, total_xp)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(guild_id, user_id) DO UPDATE SET
                    xp = EXCLUDED.xp, level = EXCLUDED.level, total_xp = EXCLUDED.total_xp
            """, (guild_id, user_id, xp, level, total_xp))
            await db.commit()
            return leveled_up

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot: return
        settings = await self.get_guild_settings(message.guild.id)
        if not settings["enabled"] or message.channel.id in settings["ignored"]: return

        if await self.award_xp(message.author, 15):
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT level FROM user_levels WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id)) as cursor:
                    row = await cursor.fetchone()
                    lvl = row[0] if row else 0
            
            responses = [
                "Congrats {user}! You are now level {level} 😎",
                "Well done {user}! You are now level {level} have a 🥇",
                "Wow you are now level {level}! good job {user}"
            ]
            msg = random.choice(responses).format(user=message.author.mention, level=lvl)
            await message.channel.send(embed=discord.Embed(description=msg, color=discord.Color.green()))

    @commands.slash_command(name="rank", description="Check your level and XP")
    async def rank_slash(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.defer()

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT xp, level, total_xp FROM user_levels WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
                row = await cursor.fetchone()
            async with db.execute("SELECT COUNT(*) FROM user_levels WHERE guild_id = ? AND total_xp > (SELECT total_xp FROM user_levels WHERE guild_id = ? AND user_id = ?)", (ctx.guild.id, ctx.guild.id, member.id)) as cursor:
                rank_row = await cursor.fetchone()
                rank = (rank_row[0] + 1) if row else "N/A"

        xp, level = (row[0], row[1]) if row else (0, 0)
        req_xp = self.get_xp_for_level(level)
        pct = min(int((xp / req_xp) * 100), 100) if req_xp > 0 else 0

        try:
            img = Image.new("RGBA", (934, 282), (35, 39, 42))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((20, 20, 914, 262), radius=15, fill=(42, 46, 53))
            
            async with httpx.AsyncClient() as client:
                resp = await client.get(member.display_avatar.url)
                avatar = Image.open(BytesIO(resp.content)).convert("RGBA").resize((160, 160))
            
            mask = Image.new("L", (160, 160), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 160, 160), fill=255)
            img.paste(avatar, (50, 50), mask)
            
            draw.rounded_rectangle((260, 180, 890, 220), radius=20, fill=(72, 75, 78))
            if pct > 0:
                draw.rounded_rectangle((260, 180, 260 + int(630 * (pct/100)), 220), radius=20, fill=(0, 250, 129))
            
            try:
                f_l = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 40)
                f_m = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 30)
            except: f_l = f_m = ImageFont.load_default()
            
            draw.text((270, 120), member.display_name, font=f_l, fill=(0, 250, 129))
            draw.text((890 - draw.textlength(f"{xp}/{req_xp} XP", f_m), 125), f"{xp}/{req_xp} XP", font=f_m, fill=(255, 255, 255))
            draw.text((890 - draw.textlength(f"Rank #{rank}  Lvl {level}", f_m), 40), f"Rank #{rank}  Lvl {level}", font=f_m, fill=(0, 250, 129))
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            await ctx.respond(file=discord.File(buf, filename="rank.png"))
        except Exception as e:
            logger.error(f"Rank error: {e}")
            await ctx.respond(embed=discord.Embed(title=f"⭐ {member.display_name}", description=f"Lvl: {level} | XP: {xp}/{req_xp} | Rank: #{rank}", color=0x00fa81))

    @commands.slash_command(name="leaderboard", description="Server top members")
    async def leaderboard_slash(self, ctx):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id, level, total_xp FROM user_levels WHERE guild_id = ? ORDER BY total_xp DESC LIMIT 10", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
        if not rows: return await ctx.respond("No activity yet!")
        desc = "\n".join([f"{i+1}. <@{r[0]}> — **Lvl {r[1]}** ({r[2]} XP)" for i, r in enumerate(rows)])
        await ctx.respond(embed=discord.Embed(title=f"🏆 {ctx.guild.name} Top 10", description=desc, color=0xFFD700))

def setup(bot):
    bot.add_cog(Leveling(bot))
