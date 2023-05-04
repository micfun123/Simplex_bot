import random
import asyncio
import discord
import aiosqlite
from discord.ext import commands 

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.database = "databases/giveaways.db"

    @commands.command()
    @commands.is_owner()
    async def makegiveawaytable(self, ctx):
        async with aiosqlite.connect("databases/giveaways.db") as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS giveaways (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER,
                message_id INTEGER,
                prize TEXT,
                winners INTEGER,
                end_time INTEGER
            );
        """)
            await db.commit()
            await ctx.send("Table created")

    async def add_giveaway(self, ctx, prize, winners, duration):
        end_time = asyncio.Future()
        await ctx.send(f"React with 🎉 to enter the giveaway for **{prize}**! Winners: **{winners}**. Time: **{duration}s**.")
        await ctx.message.add_reaction("🎉")
        reaction, _ = await self.bot.wait_for("reaction_add", check=lambda r, u: r.message == ctx.message and u != self.bot.user and str(r.emoji) == "🎉")
        message = reaction.message

        if not self.running:
            self.running = True
            self.bot.loop.create_task(self.giveaway_loop())

        await self.db.execute("INSERT INTO giveaways (channel_id, message_id, prize, winners, end_time) VALUES (?, ?, ?, ?, ?)",
                              (ctx.channel.id, message.id, prize, winners, end_time))
        await self.db.commit()

        await asyncio.sleep(duration)
        end_time.set_result(True)

    async def giveaway_loop(self):
       while True:
            async with aiosqlite.connect("databases/giveaways.db") as db:
                self.db = db
                await self.create_giveaway_table()
                rows = await self.db.execute("SELECT * FROM giveaways").fetchall()
                for row in rows:
                    if row[5] is None or row[5] > 0:
                        continue
                    channel = self.bot.get_channel(row[1])
                    message = await channel.fetch_message(row[2])
                    reactions = message.reactions
                    users = []
                    for reaction in reactions:
                        async for user in reaction.users():
                            if user.bot:
                                continue
                            users.append(user.id)
                    winners = random.sample(users, row[4])
                    if len(winners) == 0:
                        continue
                    if len(winners) == 1:
                        winner_string = "<@" + str(winners[0]) + "> is the winner!"
                    else:
                        winner_string = "The winners are:\n"
                        for winner in winners:
                            winner_string += "<@" + str(winner) + ">\n"
                    embed = discord.Embed(title=f"Giveaway Ended - {row[3]}", description=winner_string, color=0x00FF00)
                    await channel.send(embed=embed)
                    await self.db.execute("DELETE FROM giveaways WHERE id = ?", (row[0],))
                    await self.db.commit()

                await asyncio.sleep(60)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, prize, winners: int, duration: int):
        await self.add_giveaway(ctx, prize, winners, duration)

                   


    
    