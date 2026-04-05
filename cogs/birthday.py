import discord
from discord.ext import commands, tasks
from discord import option
import aiosqlite
import httpx
import os
import asyncio
import logging
from datetime import datetime, time

# Setup logging
logger = logging.getLogger("simplex.birthday")

class Birthday(commands.Cog):
    """🎂 Celebrate birthdays with the community!"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/birthdays.db"
        self.announcement_loop.start()

    def cog_unload(self):
        self.announcement_loop.cancel()

    # Slash Command Group
    birthday = discord.SlashCommandGroup("birthday", "Birthday related commands")

    @birthday.command(name="set", description="Set your birthday")
    @option("day", int, description="Day of the month (1-31)", min_value=1, max_value=31)
    @option("month", int, description="Month (1-12)", min_value=1, max_value=12)
    async def set_birthday(self, ctx, day: int, month: int):
        """Set your birthday to be celebrated by the server."""
        token = os.getenv("TOPGG_TOKEN")
        voted = 1 # Default to 1 if no token or error
        if token:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"https://top.gg/api/bots/902240397273743361/check?userId={ctx.author.id}",
                        headers={"Authorization": token},
                        timeout=10.0
                    )
                    if resp.status_code == 200:
                        voted = resp.json().get("voted", 1)
            except Exception as e:
                logger.error(f"TopGG API Error: {e}")

        if voted == 0:
            return await ctx.respond(
                "You need to have voted for Simplex in the last 24 hours to set your birthday. Vote here: https://top.gg/bot/902240397273743361/vote",
                ephemeral=True,
            )

        # Format as DD/MM
        bday_str = f"{day:02d}/{month:02d}"
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO user_birthdays (user_id, birthday) VALUES (?, ?)",
                (ctx.author.id, bday_str)
            )
            await db.commit()
            
        await ctx.respond(f"✅ Your birthday has been set to **{bday_str}**!")

    @birthday.command(name="find", description="Find a user's birthday")
    @option("user", discord.Member, description="The user to find")
    async def find_birthday(self, ctx, user: discord.Member):
        """Check when a user's birthday is."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT birthday FROM user_birthdays WHERE user_id = ?", (user.id,)) as cursor:
                row = await cursor.fetchone()
        
        if not row:
            return await ctx.respond(f"❌ {user.display_name} has not set their birthday yet.", ephemeral=True)
            
        await ctx.respond(f"🎂 {user.display_name}'s birthday is on **{row[0]}**!")

    @birthday.command(name="setup", description="Set up birthday announcements for this server")
    @commands.has_permissions(manage_guild=True)
    @option("channel", discord.TextChannel, description="The channel for birthday messages")
    @option("message", str, description="Custom birthday message (use {user} for mention)", default=None)
    async def setup_birthday(self, ctx, channel: discord.TextChannel, message: str = None):
        """Configure the birthday announcement channel and message."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO guild_config (guild_id, enabled, channel_id, message)
                VALUES (?, 1, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    channel_id = EXCLUDED.channel_id,
                    message = EXCLUDED.message,
                    enabled = 1
            """, (ctx.guild.id, channel.id, message))
            await db.commit()
            
        embed = discord.Embed(title="✅ Birthday Setup Complete", color=discord.Color.green())
        embed.add_field(name="Channel", value=channel.mention)
        embed.add_field(name="Message", value=message or "Default (:tada: Happy Birthday {user}!)")
        await ctx.respond(embed=embed)

    @birthday.command(name="toggle", description="Enable or disable birthday announcements")
    @commands.has_permissions(manage_guild=True)
    async def toggle_birthday(self, ctx):
        """Quickly turn birthday announcements on or off."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT enabled FROM guild_config WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()
            
            if not row:
                return await ctx.respond("❌ Birthday system is not set up. Use `/birthday setup` first.", ephemeral=True)
            
            new_status = 0 if row[0] == 1 else 1
            await db.execute("UPDATE guild_config SET enabled = ? WHERE guild_id = ?", (new_status, ctx.guild.id))
            await db.commit()
            
        status_text = "enabled" if new_status == 1 else "disabled"
        await ctx.respond(f"✅ Birthday announcements have been **{status_text}**.")

    @tasks.loop(time=time(hour=7, minute=0)) # Runs at 7:00 AM UTC
    async def announcement_loop(self):
        """Efficient daily loop for birthday announcements."""
        today = datetime.now().strftime("%d/%m")
        logger.info(f"Checking for birthdays today: {today}")

        async with aiosqlite.connect(self.db_path) as db:
            # 1. Get all users whose birthday is today
            async with db.execute("SELECT user_id FROM user_birthdays WHERE birthday = ?", (today,)) as cursor:
                birthday_users = await cursor.fetchall()
            
            if not birthday_users:
                return

            birthday_user_ids = [u[0] for u in birthday_users]

            # 2. Get all guilds with birthdays enabled
            async with db.execute("SELECT guild_id, channel_id, message FROM guild_config WHERE enabled = 1") as cursor:
                guilds_to_notify = await cursor.fetchall()

        for guild_id, channel_id, custom_msg in guilds_to_notify:
            guild = self.bot.get_guild(guild_id)
            if not guild: continue
            
            channel = guild.get_channel(channel_id)
            if not channel: continue

            # Find users in this guild with birthdays today
            found_users = []
            for user_id in birthday_user_ids:
                member = guild.get_member(user_id)
                if member:
                    found_users.append(member.mention)
            
            if found_users:
                msg_format = custom_msg or ":tada: Happy Birthday {user}!"
                try:
                    # If multiple birthdays, we can join them
                    mentions = ", ".join(found_users)
                    final_message = msg_format.replace("{user}", mentions)
                    await channel.send(final_message)
                except Exception as e:
                    logger.error(f"Failed to send birthday message in guild {guild_id}: {e}")
            
            # Small sleep to avoid rate limits on very large bot deployments
            await asyncio.sleep(0.1)

    @announcement_loop.before_loop
    async def before_announcement_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(name="birthdaytest")
    @commands.is_owner()
    async def birthdaytest_owner(self, ctx):
        """[Owner Only] Force-check birthdays for today."""
        await ctx.send("🔄 Running birthday check...")
        await self.announcement_loop()
        await ctx.send("✅ Check complete!")

def setup(bot):
    bot.add_cog(Birthday(bot))
