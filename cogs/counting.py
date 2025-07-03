import discord
from discord.ext import commands
import aiosqlite
from simpcalc import simpcalc
from base69 import decode_base69

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            # Parse the message content
            msg_content = message.content
            try:
                if msg_content.startswith("69*|"):
                    msg = decode_base69(msg_content)
                else:
                    calc = simpcalc.Calculate()
                    ans = await calc.calculate(msg_content)
                    msg = int(ans)
                print(f"[DEBUG] Parsed message: {msg}")
            except Exception as e:
                print(f"[ERROR] Failed to parse message: {msg_content} | Error: {e}")
                return

            async with aiosqlite.connect("./databases/counting.db") as db:
                # Enable WAL mode for better concurrency
                await db.execute("PRAGMA journal_mode=WAL")

                # Fetch current counting state
                async with await db.execute(
                    "SELECT counting_channel, lastcounter, last_user, highest, attempts FROM counting WHERE Guild_id = ?",
                    (message.guild.id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return

                    channel_id, lastcounter, last_user, highest, attempts = row
                    print(f"[DEBUG] Current state - Last: {lastcounter}, User: {last_user}, Highest: {highest}, Attempts: {attempts}")

                # Verify correct channel
                if message.channel.id != channel_id:
                    return

                # Determine expected number
                expected = 1 if lastcounter == 0 or last_user is None else lastcounter + 1
                print(f"[DEBUG] Expected number: {expected}, User's number: {msg}")

                # Check for failure conditions
                if msg != expected:
                    print("[DEBUG] Wrong number detected")
                    try:
                        await message.add_reaction("❌")
                        await message.channel.send(
                            f"Wrong number! Expected {expected}. Count reset to 0.\n"
                            f"Next number should be 1, {message.author.mention}!"
                        )
                    except discord.HTTPException as e:
                        print(f"[ERROR] Failed to add reaction: {e}")

                    async with await db.execute(
                        "UPDATE counting SET lastcounter = 0, last_user = NULL, attempts = attempts + 1 WHERE Guild_id = ?",
                        (message.guild.id,)
                    ):
                        await db.commit()

                    # Update user stats
                    async with await db.execute(
                        """
                        INSERT INTO user_count_stats (user_id, guild_id, success, failed)
                        VALUES (?, ?, 0, 1)
                        ON CONFLICT(user_id, guild_id) DO UPDATE SET failed = failed + 1
                        """,
                        (message.author.id, message.guild.id)
                    ):
                        await db.commit()
                    return

                # Check for consecutive counting
                if last_user == message.author.id:
                    print("[DEBUG] Consecutive counting detected")
                    try:
                        await message.add_reaction("❌")
                        await message.channel.send(
                            f"No consecutive counting, {message.author.mention}!\n"
                            "Count reset to 0. Next number should be 1."
                        )
                    except discord.HTTPException as e:
                        print(f"[ERROR] Failed to add reaction: {e}")

                    async with await db.execute(
                        "UPDATE counting SET lastcounter = 0, last_user = NULL, attempts = attempts + 1 WHERE Guild_id = ?",
                        (message.guild.id,)
                    ):
                        await db.commit()

                    # Update user stats
                    async with await db.execute(
                        """
                        INSERT INTO user_count_stats (user_id, guild_id, success, failed)
                        VALUES (?, ?, 0, 1)
                        ON CONFLICT(user_id, guild_id) DO UPDATE SET failed = failed + 1
                        """,
                        (message.author.id, message.guild.id)
                    ):
                        await db.commit()
                    return

                # Successful count
                print("[DEBUG] Successful count")
                try:
                    await message.add_reaction("✅")
                except discord.HTTPException as e:
                    print(f"[ERROR] Failed to add reaction: {e}")

                new_highest = max(msg, highest)
                async with await db.execute(
                    "UPDATE counting SET lastcounter = ?, last_user = ?, highest = ? WHERE Guild_id = ?",
                    (msg, message.author.id, new_highest, message.guild.id)  
                ):
                    await db.commit()
                    print(f"[DEBUG] Updated counting state - Last: {msg}, User: {message.author.id}, Highest: {new_highest}")

                    # Update user stats
                    async with await db.execute(
                        """
                        INSERT INTO user_count_stats (user_id, guild_id, success, failed)
                        VALUES (?, ?, 1, 0)
                        ON CONFLICT(user_id, guild_id) DO UPDATE SET success = success + 1
                        """,
                        (message.author.id, message.guild.id)
                    ):
                        await db.commit()

                #
                if msg > 1:
                    await message.channel.send(f"{message.author.mention} counted {msg}!")

        except Exception as e:
            print(f"[ERROR] Counting error: {type(e).__name__}: {e}")
            await message.channel.send("⚠️ An error occurred. Please try again.")

        await self.bot.process_commands(message)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel: discord.TextChannel):
        """Set the counting channel"""
        async with aiosqlite.connect("./databases/counting.db") as db:
            await db.execute("""
                INSERT OR REPLACE INTO counting 
                (Guild_id, counting_channel, lastcounter, last_user, highest, attempts)
                VALUES (?, ?, 0, NULL, 0, 0)
            """, (ctx.guild.id, channel.id))
            await db.commit()
            
        await ctx.send(
            f"✅ Counting channel set to {channel.mention}.\n"
            "The game has been reset. Start from 1!"
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setnum(self, ctx, number: int):
        """Manually set the next number to count (admin only)."""
        if number < 1:
            return await ctx.send("Number must be at least 1.")
        async with aiosqlite.connect("./databases/counting.db") as db:
            await db.execute(
                "UPDATE counting SET lastcounter = ? WHERE Guild_id = ?",
                (number - 1, ctx.guild.id)
            )
            await db.commit()
            
        await ctx.send(f"✅ Next number set. Please count **{number}** next.")

    @commands.command()
    async def countingstats(self, ctx):
        """Show server-wide counting stats"""
        async with aiosqlite.connect("./databases/counting.db") as db:
            cursor = await db.execute(
                "SELECT counting_channel, lastcounter, last_user, highest, attempts FROM counting WHERE Guild_id = ?",
                (ctx.guild.id,)
            )
            row = await cursor.fetchone()
            if not row or row[0] is None:
                return await ctx.send("❌ Counting is not configured in this server.")
            channel_id, lastcounter, last_user, highest, attempts = row

        embed = discord.Embed(
            title="📊 Counting Stats",
            color=discord.Color.green()
        )
        embed.add_field(name="Current Number", value=lastcounter, inline=True)
        embed.add_field(name="Next Number", value=lastcounter + 1, inline=True)
        embed.add_field(name="Highest Count", value=highest, inline=True)
        embed.add_field(name="Failed Attempts", value=attempts, inline=True)
        embed.add_field(name="Channel", value=f"<#{channel_id}>", inline=True)
        if last_user:
            embed.add_field(name="Last Counter", value=f"<@{last_user}>", inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countingoff(self, ctx):
        """Disable counting in this server."""
        async with aiosqlite.connect("./databases/counting.db") as db:
            await db.execute(
                "UPDATE counting SET counting_channel = NULL WHERE Guild_id = ?",
                (ctx.guild.id,)
            )
            await db.commit()
            
        await ctx.send("🛑 Counting has been disabled.")


def setup(bot):
    bot.add_cog(Counting(bot))
