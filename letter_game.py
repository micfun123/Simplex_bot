import discord
from discord.ext import commands
import asyncio
from discord import Embed
import aiosqlite

rules = """
A set of rules - No going twice 
You must go in the order of the alphabet 
You cannot repeat a word
Start with A, example Apple / Bear / cottage cheese 
Keep repeating this order until you get to Z then start over again 
If you repeat you will lose the ability to keep playing.
A staff member may reset the game
"""


class letter_game(commands.Cog):
    """The Word games"""

    def __init__(self, client):
        self.client = client

    @commands.command(name="how_to_letter_game")
    async def letter_game_rules(self, ctx):
        await ctx.respond(rules)

    @commands.is_owner()
    @commands.command(name="letter_game_db")
    async def letter_game_db(self, ctx):
        conn = await aiosqlite.connect("databases/letter_game.db")
        c = await conn.cursor()
        await c.execute(
            "CREATE TABLE IF NOT EXISTS letter_game_server (guild_id Integer, channel_id Integer, word text, last_user_id Integer, longest_game Integer, current_game Integer,total_games Integer,total_failed_games Integer)"
        )
        await conn.commit()
        await conn.close()
        await ctx.send("Done")
        conn = await aiosqlite.connect("databases/letter_game.db")
        c = await conn.cursor()
        await c.execute(
            "CREATE TABLE IF NOT EXISTS words_used (guild_id Integer, word text)"
        )
        await conn.commit()
        await conn.close()
        await ctx.send("words Done")
        conn = await aiosqlite.connect("databases/letter_game.db")
        c = await conn.cursor()
        await c.execute(
            "CREATE TABLE IF NOT EXISTS user_stats (guild_id Integer, user_id Integer, total_words Integer, Total_fails Integer)"
        )
        await conn.commit()
        await conn.close()
        await ctx.send("user stats Done")

    @commands.command(name="letter_game")
    @commands.has_permissions(manage_channels=True)
    async def letter_game_commands(self, ctx, channel: discord.TextChannel = None):
        # if bot is not at server permission highest
        if ctx.guild.me.top_role.position < ctx.author.top_role.position:
            await ctx.send(
                "I am not at the highest role position due to this I may not be able to remove users from the channel when they fail. Please consider moving my role to the top."
            )

        if channel is None:
            channel = ctx.channel

        async with aiosqlite.connect("databases/letter_game.db") as conn:
            async with conn.cursor() as c:
                await c.execute(
                    "SELECT * FROM letter_game_server WHERE guild_id = ?",
                    (ctx.guild.id,),
                )
                data = await c.fetchone()
                if data is None:
                    await c.execute(
                        "INSERT INTO letter_game_server VALUES (?,?,?,?,?,?,?,?)",
                        (ctx.guild.id, channel.id, None, 0, 0, 0, 0, 0),
                    )
                    await conn.commit()
                    await conn.close()
                    await ctx.send(
                        "Game has been started in {}".format(channel.mention)
                    )
                else:
                    await ctx.send(
                        "Game is already running in {} would you like to restart here?".format(
                            channel.mention
                        )
                    )

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        msg = await self.client.wait_for(
                            "message", timeout=30.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await ctx.send(
                            "You took to long to respond Nothing has been changed"
                        )
                    else:
                        if msg.content.lower() == "yes":
                            await c.execute(
                                "UPDATE letter_game_server SET channel_id = ?, word = ?, last_user_id = ?, longest_game = ?, current_game = ?,total_games = ?,total_failed_games = ? WHERE guild_id = ?",
                                (channel.id, None, 0, 0, 0, 0, 0, ctx.guild.id),
                            )
                            await conn.commit()
                            await conn.close()
                            await ctx.send(
                                "Game has been started in {}".format(channel.mention)
                            )
                        else:
                            await ctx.send("Nothing has been changed")

    @commands.slash_command(
        name="letter_game", description="Starts a letter game in the channel you are in"
    )
    @commands.has_permissions(manage_channels=True)
    async def letter_game_slash(self, ctx, channel: discord.TextChannel = None):
        # if bot is not at server permission highest
        if ctx.guild.me.top_role.position < ctx.author.top_role.position:
            await ctx.respond(
                "I am not at the highest role position due to this I may not be able to remove users from the channel when they fail. Please consider moving my role to the top."
            )

        if channel is None:
            channel = ctx.channel

        async with aiosqlite.connect("databases/letter_game.db") as conn:
            async with conn.cursor() as c:
                await c.execute(
                    "SELECT * FROM letter_game_server WHERE guild_id = ?",
                    (ctx.guild.id,),
                )
                data = await c.fetchone()
                if data is None:
                    await c.execute(
                        "INSERT INTO letter_game_server VALUES (?,?,?,?,?,?,?,?)",
                        (ctx.guild.id, channel.id, None, 0, 0, 0, 0, 0),
                    )
                    await conn.commit()
                    await conn.close()
                    await ctx.respond(
                        "Game has been started in {}".format(channel.mention)
                    )
                else:
                    await ctx.respond(
                        "Game is already running in {} would you like to restart here?".format(
                            channel.mention
                        )
                    )

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    try:
                        msg = await self.client.wait_for(
                            "message", timeout=30.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await ctx.respond(
                            "You took to long to respond Nothing has been changed"
                        )
                    else:
                        if msg.content.lower() == "yes":
                            await c.execute(
                                "UPDATE letter_game_server SET channel_id = ?, word = ?, last_user_id = ?, longest_game = ?, current_game = ?,total_games = ?,total_failed_games = ? WHERE guild_id = ?",
                                (channel.id, None, 0, 0, 0, 0, 0, ctx.guild.id),
                            )
                            await conn.commit()
                            await conn.close()
                            await ctx.respond(
                                "Game has been started in {}".format(channel.mention)
                            )
                        else:
                            await ctx.respond("Nothing has been changed")

    @commands.Cog.listener()
    async def on_message(self, message):
        async with aiosqlite.connect("databases/letter_game.db") as conn:
            data = await conn.execute(
                "SELECT * FROM letter_game_server WHERE guild_id = ?",
                (message.guild.id,),
            )
            data = await data.fetchone()
            if data is None:
                return
            channel_id = data[1]
            if channel_id != message.channel.id:
                print("not in channel")
                print(channel_id)
                print(message.channel.id)
                return
            print("in channel")
            print(channel_id)
            print(message.channel.id)

            if message.author.bot:
                return
            # if the message is more than 1 word
            if len(message.content.split()) > 1:
                return

            lastword = data[2]
            lastuser = data[3]
            longestgame = data[4]
            currentgame = data[5]
            totalgames = data[6]
            totalfailedgames = data[7]

            if lastuser == message.author.id:
                await message.channel.send(
                    "You can't go twice in a row. You have been removed from the game"
                )
                # remove user from channel
                await conn.execute(
                    "UPDATE letter_game_server SET total_failed_games = ? WHERE guild_id = ?",
                    (totalfailedgames + 1, message.guild.id),
                )
                await conn.commit()
                userdata = await conn.execute(
                    "SELECT * FROM user_stats WHERE user_id = ?", (message.author.id,)
                )
                userdata = await userdata.fetchone()
                if userdata is None:
                    await conn.execute(
                        "INSERT INTO user_stats VALUES (?,?,?,?,?)",
                        (message.author.id, 0, 0, 0, 0),
                    )
                    await conn.commit()
                await conn.execute(
                    "UPDATE user_stats SET letter_game_failed = ? WHERE user_id = ?",
                    (userdata[4] + 1, message.author.id),
                )
                await conn.commit()
                try:
                    await message.channel.set_permissions(
                        message.author, send_messages=False
                    )
                except discord.Forbidden:
                    await message.channel.send(
                        "I do not have permission to remove users from the channel"
                    )
                return
            if lastword is None:
                # if message does not start with a
                if message.content[0].lower() != "a":
                    await message.channel.send("The word must start with a")
                    return
                # set first current_game  total_games
                await conn.execute(
                    "UPDATE letter_game_server SET word = ?, last_user_id = ?, current_game = ?, total_games = ? WHERE guild_id = ?",
                    (
                        message.content.lower(),
                        message.author.id,
                        currentgame + 1,
                        totalgames + 1,
                        message.guild.id,
                    ),
                )
                await conn.commit()
                await conn.execute(
                    "insert into wordbank VALUES (?,?)",
                    (message.guild.id, message.content.lower()),
                )
                await conn.commit()
                await message.add_reaction("✅")
                return
            elif lastword.content[0] == "z":
                if message.content[0].lower() == "a":
                    # set first current_game  total_games
                    await conn.execute(
                        "UPDATE letter_game_server SET word = ?, last_user_id = ?, current_game = ?, total_games = ? WHERE guild_id = ?",
                        (
                            message.content.lower(),
                            message.author.id,
                            currentgame + 1,
                            totalgames + 1,
                            message.guild.id,
                        ),
                    )
                    await conn.commit()
                    await conn.execute(
                        "insert into wordbank VALUES (?,?)",
                        (message.guild.id, message.content.lower()),
                    )
                    await conn.commit()
                    await message.add_reaction("✅")
                    return
                else:
                    await message.channel.send("The word must start with a")
                    # remove user from channel
                    await conn.execute(
                        "UPDATE letter_game_server SET total_failed_games = ? WHERE guild_id = ?",
                        (totalfailedgames + 1, message.guild.id),
                    )
                    await conn.commit()
                    userdata = await conn.execute(
                        "SELECT * FROM user_stats WHERE user_id = ?",
                        (message.author.id,),
                    )
                    userdata = await userdata.fetchone()
                    if userdata is None:
                        await conn.execute(
                            "INSERT INTO user_stats VALUES (?,?,?,?,?)",
                            (message.author.id, 0, 0, 0, 0),
                        )
                        await conn.commit()
                    await conn.execute(
                        "UPDATE user_stats SET letter_game_failed = ? WHERE user_id = ?",
                        (userdata[4] + 1, message.author.id),
                    )
                    await conn.commit()
                    try:
                        await message.channel.set_permissions(
                            message.author, send_messages=False
                        )
                    except discord.Forbidden:
                        await message.channel.send(
                            "I do not have permission to remove users from the channel"
                        )
                    return
            # if this word first letter is one bigger than first letter of last word
            elif ord(message.content[0].lower()) == ord(lastword.content[-1]) + 1:
                await conn.execute(
                    "insert into wordbank VALUES (?,?)",
                    (message.guild.id, message.content.lower()),
                )
                await conn.commit()
                await conn.execute(
                    "UPDATE letter_game_server SET word = ?, last_user_id = ? WHERE guild_id = ?",
                    (message.content.lower(), message.author.id, message.guild.id),
                )
                await conn.commit()
                await message.add_reaction("✅")
                return
            else:
                await message.channel.send(
                    "the next word must start {}".format(
                        chr(ord(lastword.content[-1]) + 1)
                    )
                )
                # remove user from channel
                await conn.execute(
                    "UPDATE letter_game_server SET total_failed_games = ? WHERE guild_id = ?",
                    (totalfailedgames + 1, message.guild.id),
                )
                await conn.commit()
                userdata = await conn.execute(
                    "SELECT * FROM user_stats WHERE user_id = ?", (message.author.id,)
                )
                userdata = await userdata.fetchone()
                if userdata is None:
                    await conn.execute(
                        "INSERT INTO user_stats VALUES (?,?,?,?,?)",
                        (message.author.id, 0, 0, 0, 0),
                    )
                    await conn.commit()
                await conn.execute(
                    "UPDATE user_stats SET letter_game_failed = ? WHERE user_id = ?",
                    (userdata[4] + 1, message.author.id),
                )
                await conn.commit()
                try:
                    await message.channel.set_permissions(
                        message.author, send_messages=False
                    )
                except discord.Forbidden:
                    await message.channel.send(
                        "I do not have permission to remove users from the channel"
                    )
                return


def setup(client):
    client.add_cog(letter_game(client))
