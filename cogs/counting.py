import discord
from discord.ext import commands
from discord import option
import aiosqlite
import asyncio
import logging
from simpcalc.simpcalc import Calculate

# Setup logging
logger = logging.getLogger("simplex.counting")

class Counting(commands.Cog):
    """🎲 A fun counting game for each server!"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./databases/counting.db"
        self.guild_locks = {}   # {guild_id: asyncio.Lock}
        self.calc = Calculate()

    def get_lock(self, guild_id):
        if guild_id not in self.guild_locks:
            self.guild_locks[guild_id] = asyncio.Lock()
        return self.guild_locks[guild_id]

    async def parse_number(self, content):
        """Uses simpcalc to parse the number from message content."""
        try:
            # Strip potential code block formatting or whitespace
            expr = content.strip().strip('`').strip()
            # simpcalc is async and uses math.js API
            result_str = await self.calc.calculate(expr)
            
            # math.js can return complex numbers or other strings, we want a clean float/int
            # remove quotes if any
            result_str = result_str.strip('"').strip("'")
            
            try:
                result = float(result_str)
                # Ensure it's a whole number for counting
                if result == int(result):
                    return int(result)
            except ValueError:
                return None
            return None
        except Exception:
            return None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # Check if message is in a counting channel first to avoid unnecessary API calls
        async with self.get_lock(message.guild.id):
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT channel_id, current_number, last_user_id, highest_number FROM counting WHERE guild_id = ?", (message.guild.id,)) as cursor:
                    row = await cursor.fetchone()

                if not row or row[0] != message.channel.id:
                    return # Not a counting channel

                current_num, last_user, highest_num = row[1], row[2], row[3]
                
                # Now parse the number since we know it's a counting channel
                msg_number = await self.parse_number(message.content)
                if msg_number is None:
                    return

                expected = current_num + 1
                reaction_is = None

                try:
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
                        # Update user stats
                        await db.execute("""
                            INSERT INTO user_counts (guild_id, user_id, count)
                            VALUES (?, ?, 1)
                            ON CONFLICT(guild_id, user_id) DO UPDATE SET count = count + 1
                        """, (message.guild.id, message.author.id))
                        
                        await db.commit()
                        reaction_is = "✅"
                except Exception as e:
                    print(f"❌ Error in counting logic: {e}")

        if reaction_is:
            try:
                await message.add_reaction(reaction_is)
            except Exception as e:
                print(f"❌ Failed to add reaction: {e}")

    # Slash Command Group
    counting = discord.SlashCommandGroup("counting", "Counting game commands")

    @counting.command(name="setchannel")
    @commands.has_permissions(administrator=True)
    async def setchannel_slash(self, ctx, channel: discord.TextChannel):
        """Set the counting channel for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO counting (guild_id, channel_id, current_number, last_user_id, highest_number)
                VALUES (?, ?, 0, NULL, 0)
                ON CONFLICT(guild_id) DO UPDATE SET channel_id = EXCLUDED.channel_id, current_number = 0, last_user_id = NULL
            """, (ctx.guild.id, channel.id))
            await db.commit()
        await ctx.respond(f"✅ Counting channel set to {channel.mention}. Game reset! Start with **1**.")

    @counting.command(name="stats")
    async def stats_slash(self, ctx):
        """Show the server's counting statistics."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT current_number, highest_number, channel_id FROM counting WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

        if not row or row[2] is None:
            return await ctx.respond("❌ Counting is not set up on this server.")

        current, highest, channel_id = row
        embed = discord.Embed(title=f"📊 {ctx.guild.name} Counting Stats", color=discord.Color.blue())
        embed.add_field(name="Current Count", value=f"**{current}**", inline=True)
        embed.add_field(name="Highest Ever", value=f"**{highest}**", inline=True)
        channel = ctx.guild.get_channel(channel_id)
        embed.add_field(name="Channel", value=channel.mention if channel else "Unknown", inline=False)
        await ctx.respond(embed=embed)

    @counting.command(name="userstats")
    async def userstats_slash(self, ctx, user: discord.Member = None):
        """Show counting statistics for a specific user."""
        user = user or ctx.author
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT count FROM user_counts WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, user.id)) as cursor:
                row = await cursor.fetchone()

        count = row[0] if row else 0
        embed = discord.Embed(title=f"👤 {user.display_name}'s Counting Stats", color=discord.Color.green())
        embed.add_field(name="Correct Counts", value=f"**{count}**")
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @counting.command(name="leaderboard")
    async def leaderboard_slash(self, ctx):
        """Show the top counters in this server."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT user_id, count FROM user_counts WHERE guild_id = ? ORDER BY count DESC LIMIT 10", 
                (ctx.guild.id,)
            ) as cursor:
                rows = await cursor.fetchall()

        if not rows:
            return await ctx.respond("❌ No one has started counting yet!")

        embed = discord.Embed(title=f"🏆 {ctx.guild.name} Counting Leaderboard", color=discord.Color.gold())
        description = ""
        for i, (user_id, count) in enumerate(rows, 1):
            user = self.bot.get_user(user_id)
            user_name = user.mention if user else f"Unknown User ({user_id})"
            description += f"{i}. {user_name} — **{count}**\n"
        
        embed.description = description
        await ctx.respond(embed=embed)

    # Keep original prefix commands for compatibility
    @commands.command(name="setcountchannel")
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel: discord.TextChannel):
        """Set the counting channel for this server."""
        await self.setchannel_slash(ctx, channel)

    @commands.command(name="countstats")
    async def countstats(self, ctx):
        """Show the server's counting high score."""
        await self.stats_slash(ctx)

def setup(bot):
    bot.add_cog(Counting(bot))
