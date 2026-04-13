import discord
from discord.ext import commands
from discord import option
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

    async def parse_number(self, content):
        """Uses simpcalc to parse the number from message content."""
        return int(content.strip())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        # Check if message is in a counting channel first to avoid unnecessary API calls
        async with self.get_lock(message.guild.id):
            async with aiosqlite.connect(self.db_path) as db:
                # Actual columns: guild_id, counting_channel, lastcounter, highest, last_user, attemps, channel_id
                async with db.execute("SELECT counting_channel, lastcounter, last_user, highest FROM counting WHERE guild_id = ?", (message.guild.id,)) as cursor:
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
                        await db.execute("UPDATE counting SET lastcounter = 0, last_user = NULL WHERE guild_id = ?", (message.guild.id,))
                        
                        # Increment user failures
                        await db.execute("""
                            INSERT INTO user_counts (guild_id, user_id, count, failures)
                            VALUES (?, ?, 0, 1)
                            ON CONFLICT(guild_id, user_id) DO UPDATE SET failures = failures + 1
                        """, (message.guild.id, message.author.id))
                        
                        await db.commit()
                        reaction_is = "❌"
                    
                    # 2. Check if the number is correct
                    elif msg_number != expected:
                        await message.channel.send(f"❌ **Wrong number!** {message.author.mention} reset the count to 0. Expected **{expected}**.")
                        await db.execute("UPDATE counting SET lastcounter = 0, last_user = NULL WHERE guild_id = ?", (message.guild.id,))
                        
                        # Increment user failures
                        await db.execute("""
                            INSERT INTO user_counts (guild_id, user_id, count, failures)
                            VALUES (?, ?, 0, 1)
                            ON CONFLICT(guild_id, user_id) DO UPDATE SET failures = failures + 1
                        """, (message.guild.id, message.author.id))
                        
                        await db.commit()
                        reaction_is = "❌"

                    # 3. Correct!
                    else:
                        new_highest = max(msg_number, highest_num)
                        await db.execute(
                            "UPDATE counting SET lastcounter = ?, last_user = ?, highest = ? WHERE guild_id = ?",
                            (msg_number, message.author.id, new_highest, message.guild.id)
                        )
                        # Update user stats
                        await db.execute("""
                            INSERT INTO user_counts (guild_id, user_id, count, failures)
                            VALUES (?, ?, 1, 0)
                            ON CONFLICT(guild_id, user_id) DO UPDATE SET count = count + 1
                        """, (message.guild.id, message.author.id))
                        
                        await db.commit()
                        reaction_is = "✅"
                except Exception as e:
                    print(f"❌ Error in counting logic: {e}")

        
        if reaction_is:
            try:
                await asyncio.wait_for(message.add_reaction(reaction_is), timeout=4.0)
                print(f"✅ Successfully reacted {reaction_is} in {message.guild.id}")
                
            except asyncio.TimeoutError:
                logger.warning(f"⏰ Reaction timed out in guild {message.guild.id}")
            except discord.Forbidden:
                logger.warning(f"🚫 Missing 'Add Reactions' or 'Read Message History' in {message.guild.id}")
            except discord.HTTPException as e:
                logger.warning(f"❌ HTTP Error {e.status} ({e.text}) in {message.guild.id}")
            except Exception as e:
                logger.warning(f"❓ Unexpected error: {type(e).__name__}: {e}")

    # Slash Command Group
    counting = discord.SlashCommandGroup("counting", "Counting game commands")


    @counting.command(name="setchannel")
    @commands.has_permissions(manage_guild=True)
    async def setcountingchannel_slash(self, ctx, channel: discord.TextChannel):
        """Set the counting channel for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT 1 FROM counting WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                exists = await cursor.fetchone()

            if exists:
                await db.execute(
                    "UPDATE counting SET counting_channel = ? WHERE guild_id = ?",
                    (channel.id, ctx.guild.id)
                )
            else:
                await db.execute(
                    "INSERT INTO counting (guild_id, counting_channel, lastcounter, highest, last_user) VALUES (?, ?, 0, 0, NULL)",
                    (ctx.guild.id, channel.id)
                )
            await db.commit()
        await ctx.respond(f"✅ Counting channel has been set to {channel.mention}.")

    @counting.command(name="stats")
    async def stats_slash(self, ctx):
        """Show the server's counting statistics."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT lastcounter, highest, counting_channel FROM counting WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()
            
            # Calculate total accuracy
            async with db.execute("SELECT SUM(count), SUM(failures) FROM user_counts WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                accuracy_row = await cursor.fetchone()

        if not row or row[2] is None:
            return await ctx.respond("❌ Counting is not set up on this server.")

        current, highest, channel_id = row
        total_count = accuracy_row[0] or 0
        total_failures = accuracy_row[1] or 0
        total_attempts = total_count + total_failures
        accuracy = (total_count / total_attempts * 100) if total_attempts > 0 else 0

        embed = discord.Embed(title=f"📊 {ctx.guild.name} Counting Stats", color=discord.Color.blue())
        embed.add_field(name="Current Count", value=f"**{current}**", inline=True)
        embed.add_field(name="Highest Ever", value=f"**{highest}**", inline=True)
        embed.add_field(name="Total Attempts", value=f"**{total_attempts}**", inline=True)
        embed.add_field(name="Accuracy", value=f"**{accuracy:.1f}%**", inline=True)
        
        channel = ctx.guild.get_channel(channel_id)
        embed.add_field(name="Channel", value=channel.mention if channel else "Unknown", inline=False)
        await ctx.respond(embed=embed)

    @counting.command(name="userstats")
    async def userstats_slash(self, ctx, user: discord.Member = None):
        """Show counting statistics for a specific user."""
        user = user or ctx.author
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT count, failures FROM user_counts WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, user.id)) as cursor:
                row = await cursor.fetchone()

        count = row[0] if row else 0
        failures = row[1] if row else 0
        total = count + failures
        accuracy = (count / total * 100) if total > 0 else 0

        embed = discord.Embed(title=f"👤 {user.display_name}'s Counting Stats", color=discord.Color.green())
        embed.add_field(name="Correct Counts", value=f"**{count}**", inline=True)
        embed.add_field(name="Failures", value=f"**{failures}**", inline=True)
        embed.add_field(name="Accuracy", value=f"**{accuracy:.1f}%**", inline=True)
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @counting.command(name="leaderboard")
    async def leaderboard_slash(self, ctx):
        """Show the top counters in this server."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT user_id, count, failures FROM user_counts WHERE guild_id = ? ORDER BY count DESC LIMIT 10", 
                (ctx.guild.id,)
            ) as cursor:
                rows = await cursor.fetchall()

        if not rows:
            return await ctx.respond("❌ No one has started counting yet!")

        embed = discord.Embed(title=f"🏆 {ctx.guild.name} Counting Leaderboard", color=discord.Color.gold())
        description = ""
        for i, (user_id, count, failures) in enumerate(rows, 1):
            user = self.bot.get_user(user_id)
            user_name = user.mention if user else f"Unknown User ({user_id})"
            total = count + failures
            accuracy = (count / total * 100) if total > 0 else 0
            description += f"{i}. {user_name} — **{count}** counts ({accuracy:.0f}% accuracy)\n"
        
        embed.description = description
        await ctx.respond(embed=embed)


    @commands.command(name="countstats")
    async def countstats(self, ctx):
        """Show the server's counting high score."""
        await self.stats_slash(ctx)

def setup(bot):
    bot.add_cog(Counting(bot))
