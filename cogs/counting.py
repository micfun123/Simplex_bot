import discord
from discord.ext import commands
import aiosqlite
import asyncio
import logging

# Setup logging
logger = logging.getLogger("simplex.counting")

class Counting(commands.Cog):
    """🎲 A fun counting game for each server!"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./databases/counting.db"
        self.guild_locks = {}   # {guild_id: asyncio.Lock}

    def get_lock(self, guild_id):
        if guild_id not in self.guild_locks:
            self.guild_locks[guild_id] = asyncio.Lock()
        return self.guild_locks[guild_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # Simple integer check
        content = message.content.strip()
        if not content.isdigit():
            return

        msg_number = int(content)
        reaction_is = None

        async with self.get_lock(message.guild.id):
            try:
                async with aiosqlite.connect(self.db_path) as db:
                    # Explicitly disable WAL for this connection
                    await db.execute("PRAGMA journal_mode=DELETE")
                    await db.execute("PRAGMA synchronous=FULL")
                    
                    async with db.execute("SELECT channel_id, current_number, last_user_id, highest_number FROM counting WHERE guild_id = ?", (message.guild.id,)) as cursor:
                        row = await cursor.fetchone()

                    if not row or row[0] != message.channel.id:
                        return # Not a counting channel

                    current_num, last_user, highest_num = row[1], row[2], row[3]
                    expected = current_num + 1

                    # 1. Check if it's the same user
                    if last_user == message.author.id:
                        await message.channel.send(f"❌ {message.author.mention}, you can't count twice in a row! Count reset to 0.")
                        await db.execute("UPDATE counting SET current_number = 0, last_user_id = NULL WHERE guild_id = ?", (message.guild.id,))
                        await db.commit()
                        reaction_is = "❌"
                    
                    # 2. Check if the number is correct
                    elif msg_number != expected:
                        await message.channel.send(f"❌ **Wrong number!** {message.author.mention} reset the count to 0. Expected **{expected}**.")
                        await db.execute("UPDATE counting SET current_number = 0, last_user_id = NULL WHERE guild_id = ?", (message.guild.id,))
                        await db.commit()
                        reaction_is = "❌"

                    # 3. Correct!
                    else:
                        new_highest = max(msg_number, highest_num)
                        await db.execute(
                            "UPDATE counting SET current_number = ?, last_user_id = ?, highest_number = ? WHERE guild_id = ?",
                            (msg_number, message.author.id, new_highest, message.guild.id)
                        )
                        await db.commit()
                        reaction_is = "✅"

        
                        

            except Exception as e:
                print(f"❌ Error in counting on_message: {e}")
        
        if reaction_is:
            try:
                await message.add_reaction(reaction_is)
            except Exception as e:
                print(f"❌ Failed to add reaction: {e}")





    @commands.command(name="setcountchannel")
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel: discord.TextChannel):
        """Set the counting channel for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=DELETE")
            await db.execute("""
                INSERT INTO counting (guild_id, channel_id, current_number, last_user_id, highest_number)
                VALUES (?, ?, 0, NULL, 0)
                ON CONFLICT(guild_id) DO UPDATE SET channel_id = EXCLUDED.channel_id, current_number = 0, last_user_id = NULL
            """, (ctx.guild.id, channel.id))
            await db.commit()
        
        await ctx.send(f"✅ Counting channel set to {channel.mention}. Game reset! Start with **1**.")

    @commands.command(name="forcestart")
    @commands.is_owner()
    async def forcestart(self, ctx, channel: discord.TextChannel):
        """[Owner Only] Force-set the counting channel."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=DELETE")
            await db.execute("""
                INSERT INTO counting (guild_id, channel_id, current_number, last_user_id, highest_number)
                VALUES (?, ?, 0, NULL, 0)
                ON CONFLICT(guild_id) DO UPDATE SET channel_id = EXCLUDED.channel_id, current_number = 0, last_user_id = NULL
            """, (ctx.guild.id, channel.id))
            await db.commit()
        
        await ctx.send(f"🛠️ **[FORCE]** Counting channel set to {channel.mention}. Start from **1**!")

    @commands.command(name="countstats")
    async def countstats(self, ctx):
        """Show the server's counting high score."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT current_number, highest_number, channel_id FROM counting WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

        if not row or row[2] is None:
            return await ctx.send("❌ Counting is not set up.")

        current, highest, channel_id = row
        embed = discord.Embed(title="📊 Counting Statistics", color=discord.Color.blue())
        embed.add_field(name="Current Count", value=f"**{current}**")
        embed.add_field(name="Highest Ever", value=f"**{highest}**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Counting(bot))
