import discord
from discord.ext import commands, tasks
from discord import option
import random
import httpx
import aiosqlite
import os
from datetime import datetime, time
import logging

# Setup logging
logger = logging.getLogger("simplex.qotd")

TRIVIA_URL = "https://the-trivia-api.com/api/questions?categories=society_and_culture,arts_and_literature,film_and_tv,food_and_drink,general_knowledge,geography,history,music,science&limit=1&difficulty=medium"

class QOTD(commands.Cog):
    """Daily trivia questions for your server!"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/qotd.db"
        self.answer_path = "databases/qotd.txt"
        self.qotd_loop.start()

    def cog_unload(self):
        self.qotd_loop.cancel()

    # Slash Command Group
    qotd = discord.SlashCommandGroup("qotd", "Daily trivia commands")

    @qotd.command(name="setup", description="Set up Question of the Day")
    @commands.has_permissions(administrator=True)
    @option("channel", discord.TextChannel, description="The channel for QOTD")
    @option("role", discord.Role, description="Optional role to ping when a new QOTD is posted", default=None)
    async def setup_qotd(self, ctx, channel: discord.TextChannel, role: discord.Role = None):
        """Enable or update QOTD for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO qotd (server_id, channel_id, role_id)
                VALUES (?, ?, ?)
                ON CONFLICT(server_id) DO UPDATE SET
                    channel_id = EXCLUDED.channel_id,
                    role_id = EXCLUDED.role_id
            """, (ctx.guild.id, channel.id, role.id if role else None))
            await db.commit()
            
        embed = discord.Embed(title="✅ QOTD Enabled", color=discord.Color.green())
        embed.add_field(name="Channel", value=channel.mention)
        if role:
            embed.add_field(name="Ping Role", value=role.mention)
        
        await ctx.respond(embed=embed)
        await ctx.followup.send(
            "If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361\nIt helps a lot! :D",
            ephemeral=True,
        )

    @qotd.command(name="disable", description="Disable Question of the Day")
    @commands.has_permissions(administrator=True)
    async def disable_qotd(self, ctx):
        """Stop sending trivia questions to this server."""
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
                "You need to have voted for Simplex in the last 24 hours to disable this. Vote here: https://top.gg/bot/902240397273743361/vote",
                ephemeral=True,
            )

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM qotd WHERE server_id = ?", (ctx.guild.id,)) as cursor:
                if not await cursor.fetchone():
                    return await ctx.respond("❌ QOTD is already disabled on this server!", ephemeral=True)
            
            await db.execute("DELETE FROM qotd WHERE server_id = ?", (ctx.guild.id,))
            await db.commit()
            
        await ctx.respond("🗑️ QOTD has been disabled.")
        await ctx.followup.send(
            "If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361\nIt helps a lot! :D",
            ephemeral=True,
        )

    async def send_qotd(self, ctx=None):
        """Fetch and send the daily trivia question."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(TRIVIA_URL, timeout=15.0)
                data = resp.json()
                
            if not data:
                return

            trivia = data[0]
            question = trivia["question"]
            correct_answer = trivia["correctAnswer"]
            options = trivia["incorrectAnswers"]
            options.append(correct_answer)
            random.shuffle(options)

            # Get yesterday's answer from file
            yesterday_answer = "N/A"
            if os.path.exists(self.answer_path):
                with open(self.answer_path, "r") as f:
                    yesterday_answer = f.read().strip() or "N/A"

            # Save today's answer
            with open(self.answer_path, "w") as f:
                f.write(correct_answer)

            # Iterate through servers
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT server_id, channel_id, role_id FROM qotd") as cursor:
                    servers = await cursor.fetchall()

            for server_id, channel_id, role_id in servers:
                try:
                    channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
                    if not channel:
                        continue

                    embed = discord.Embed(title="🎲 Question of the Day", description=f"**{question}**", color=0x00FF00)
                    embed.add_field(
                        name="Options",
                        value="\n".join([f"• {opt}" for opt in options]),
                        inline=False
                    )
                    embed.add_field(
                        name="Yesterday's Answer",
                        value=f"||{yesterday_answer}||",
                        inline=False
                    )
                    embed.set_footer(text=f"QOTD for {datetime.now().strftime('%d/%m/%Y')}\nThanks for supporting Simplex!")
                    
                    content = ""
                    if role_id:
                        role = channel.guild.get_role(role_id)
                        if role:
                            content = role.mention

                    await channel.send(content=content, embed=embed)
                except Exception as e:
                    logger.error(f"Failed to send QOTD to {server_id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error in send_qotd: {e}")

    @tasks.loop(time=time(hour=0, minute=0)) # Runs at midnight UTC
    async def qotd_loop(self):
        await self.send_qotd()

    @qotd_loop.before_loop
    async def before_qotd_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(name="qotdtest")
    @commands.is_owner()
    async def qotdtest_command(self, ctx):
        """[Owner Only] Force-send the QOTD to all servers."""
        await ctx.send("🔄 Sending QOTD to all servers...")
        await self.send_qotd()
        await ctx.send("✅ Done!")

def setup(bot):
    bot.add_cog(QOTD(bot))
