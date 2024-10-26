from tools import mic, log
import json
from discord import Guild, Option
import discord
from discord.ext import commands
import discord.ui
import calendar, datetime, time
import sqlite3
import aiosqlite


async def get_data_announcement():
    with open("./databases/announcement.json") as f:
        data = json.load(f)
    return data


async def dump_data_announcement(data):
    with open("./databases/announcement.json", "w") as f:
        json.dump(data, f, indent=4)


async def get_data():
    con = sqlite3.connect("databases/log.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM log")
    data = cur.fetchall()
    return data


async def dump_data(data):
    with open("./databases/log.json", "w") as f:
        json.dump(data, f, indent=4)


class Moderationsettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def announcement_all(self, ctx, *, message):
        sentto = 0
        # get all servers
        con = sqlite3.connect("databases/announcement.db")
        cur = con.cursor()
        for i in self.client.guilds:
            data = cur.execute(
                "SELECT * FROM server WHERE ServerID = ?", (i.id,)
            ).fetchone()
            try:
                channel = self.client.get_channel(data[1])
                await channel.send(message)
            except Exception:
                try:
                    system_channel = i.system_channel
                    await system_channel.send(message)
                    sentto += 1
                except Exception:
                    pass
        await ctx.send(f"Sent to {sentto} servers")

    @commands.command()
    @commands.is_owner()
    async def announcement(self, ctx, *,message):
        # get all servers
        con = sqlite3.connect("databases/announcement.db")
        cur = con.cursor()
        total = 0
        for i in self.client.guilds:
            try:
                data = cur.execute(
                    "SELECT * FROM server WHERE ServerID = ?", (i.id,)
                ).fetchone()
                try:
                    channel = self.client.get_channel(data[1])
                    #if there was a image in the message
                    if ctx.message.attachments:
                        await channel.send(message, file=await ctx.message.attachments[0].to_file())

                    else:
                        await channel.send(message)
                    total += 1
                except Exception as e:
                    print(f"Failed to send announcement to {i.name}: {e}")
            except Exception as e:
                print(f"Failed to fetch data for server {i.name}: {e}")

        await ctx.send(f"Sent to {total} out of {len(self.client.guilds)} servers")

    @commands.command()
    @commands.is_owner()
    async def announcement_embed(self, ctx, titel, *, message):
        # estimate time to send to all servers
        time_to_send = len(self.client.guilds) * 0.05
        await ctx.send(f"Estimated time to send to all servers: {time_to_send} seconds")
        con = sqlite3.connect("databases/announcement.db")
        cur = con.cursor()
        total = 0
        embed = discord.Embed(title=titel, description=message, color=0x00FF00)
        for i in self.client.guilds:
            data = cur.execute(
                "SELECT * FROM server WHERE ServerID = ?", (i.id,)
            ).fetchone()
            try:
                channel = self.client.get_channel(data[1])
                await channel.send(embed=embed)
                total += 1
            except Exception:
                pass
        await ctx.send(f"Sent to {total} out of {self.client.guilds} servers")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setLogChannel(self, ctx, channel: discord.TextChannel):
        # connect to sql
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM log WHERE GuildID=?", (ctx.guild.id,)
        ).fetchone()
        if data:
            cur.execute(
                "UPDATE log SET ChannelID=? WHERE GuildID=?", (channel.id, ctx.guild.id)
            )
            con.commit()
            await ctx.send(f"Set log channel to {channel.mention}")
        else:
            cur.execute("INSERT INTO log VALUES (?, ?)", (ctx.guild.id, channel.id))
            con.commit()
            await ctx.send(f"Set log channel to {channel.mention}")

    
    @commands.slash_command(description = "Set the log channel for the server. All server logs will be sent to this channel")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        # connect to sql
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM log WHERE GuildID=?", (ctx.guild.id,)
        ).fetchone()
        if data:
            cur.execute(
                "UPDATE log SET ChannelID=? WHERE GuildID=?", (channel.id, ctx.guild.id)
            )
            con.commit()
            await ctx.send(f"Set log channel to {channel.mention}")
        else:
            cur.execute("INSERT INTO log VALUES (?, ?)", (ctx.guild.id, channel.id))
            con.commit()
            await ctx.send(f"Set log channel to {channel.mention}")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_announcment_channel(self, ctx, channel: discord.TextChannel):
        await ctx.send("This connecting")
        con = sqlite3.connect("databases/announcement.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM server WHERE ServerID=?", (ctx.guild.id,))
        data = data.fetchall()
        if data:
            cur.execute(
                "UPDATE server SET channel=? WHERE ServerID=?",
                (channel.id, ctx.guild.id),
            )
            con.commit()
            await ctx.send(f"Set announcement channel to {channel.mention}")
        else:
            cur.execute("INSERT INTO server VALUES (?, ?)", (ctx.guild.id, channel.id))
            con.commit()
            await ctx.send(f"Set announcement channel to {channel.mention}")

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def announcement_channel(self, ctx, channel: discord.TextChannel):
        con = sqlite3.connect("databases/announcement.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM server WHERE ServerID=?", (ctx.guild.id,))
        data = data.fetchall()
        if data:
            cur.execute(
                "UPDATE server SET channel=? WHERE ServerID=?",
                (channel.id, ctx.guild.id),
            )
            con.commit()
            await ctx.respond(f"Set announcement channel to {channel.mention}")
        else:
            cur.execute("INSERT INTO server VALUES (?, ?)", (ctx.guild.id, channel.id))
            con.commit()
            await ctx.respond(f"Set announcement channel to {channel.mention}")



    ## THESE ARE THE LOGGING EVENTS ##
    @commands.command()
    @commands.is_owner()
    async def add_bot_column(self, ctx):
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        cur.execute("ALTER TABLE log ADD COLUMN log_bot boolean")
        con.commit()
        await ctx.send("Added bot column")
        #set all to true
        cur.execute("UPDATE log SET log_bot = 1")
        con.commit()
        
    @commands.command(help="Toggle logging for bots")
    @commands.has_permissions(administrator=True)
    async def toggle_bot_loger(self, ctx):
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM log WHERE GuildID=?", (ctx.guild.id,)).fetchone()
        if data:
            if data[2] == 1:
                cur.execute("UPDATE log SET log_bot = 0 WHERE GuildID=?", (ctx.guild.id,))
                con.commit()
                await ctx.send("Disabled bot logging")
            else:
                cur.execute("UPDATE log SET log_bot = 1 WHERE GuildID=?", (ctx.guild.id,))
                con.commit()
                await ctx.send("Enabled bot logging")
        else:
            await ctx.send("Please set a log channel first")

    @commands.slash_command(help="Toggle logging for bots")
    @commands.has_permissions(administrator=True)
    async def toggle_bot_logging(self, ctx):
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM log WHERE GuildID=?", (ctx.guild.id,)).fetchone()
        if data:
            if data[2] == 1:
                cur.execute("UPDATE log SET log_bot = 0 WHERE GuildID=?", (ctx.guild.id,))
                con.commit()
                await ctx.respond("Disabled bot logging")
            else:
                cur.execute("UPDATE log SET log_bot = 1 WHERE GuildID=?", (ctx.guild.id,))
                con.commit()
                await ctx.respond("Enabled bot logging")
        else:
            await ctx.respond("Please set a log channel first")












    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.client.user.id:
            return
        if before.content == after.content:
            return

        em = discord.Embed(
            color=discord.Color.blue(),
            title="Message Edit",
            description=f"{before.author} edited their message",
        )
        em.add_field(name="Before", value=before.content)
        em.add_field(name="After", value=after.content)
        em.add_field(name="Channel", value=after.channel)
        em.add_field(
            name="Link",
            value=f"https://discordapp.com/channels/{after.guild.id}/{after.channel.id}/{after.id}",
        )
        em.add_field(name="Time", value=after.created_at)

        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        async with aiosqlite.connect("databases/log.db") as con:
            cur = await con.execute(
                "SELECT * FROM log WHERE GuildID=?", (after.guild.id,)
            )
            data = await cur.fetchone()
        if data:
            if data[2] == 0 and after.author.bot:
                return
            channel = self.client.get_channel(data[1])
            await channel.send(embed=em)
        else:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.nick is not None and after.nick is None:
                em = discord.Embed(
                    color=discord.Color.blue(),
                    title="Nick Change",
                    description=f"{before.name} has unicked",
                    timestamp=datetime.datetime.utcnow(),
                )
                em.add_field(name="Before:", value=before.nick)
                em.add_field(name="After:", value="No Nick")
                async with aiosqlite.connect("databases/log.db") as con:
                    cur = await con.execute(
                        "SELECT * FROM log WHERE GuildID=?", (before.guild.id,)
                    )
                    data = await cur.fetchone()
                if data:
                    if data[2] == 0 and before.bot:
                        return
                    channel = self.client.get_channel(data[1])
                    await channel.send(embed=em)
                    return

            if before.nick is None and after.nick is not None:
                em = discord.Embed(
                    color=discord.Color.blue(),
                    title="Nick Change",
                    description=f"{before.name} Has nicked",
                    timestamp=datetime.datetime.utcnow(),
                )
                em.add_field(name="Before:", value="No Nick")
                em.add_field(name="After:", value=after.nick)
                async with aiosqlite.connect("databases/log.db") as con:
                    cur = await con.execute(
                        "SELECT * FROM log WHERE GuildID=?", (before.guild.id,)
                    )
                    data = await cur.fetchone()
                if data:
                    if data[2] == 0 and before.bot:
                        return
                    channel = self.client.get_channel(data[1])
                    await channel.send(embed=em)
                    return

            elif before.nick != after.nick:
                em = discord.Embed(
                    color=discord.Color.blue(),
                    title="Nick Change",
                    description=f"{before.name} Has changed their nick",
                    timestamp=datetime.datetime.utcnow(),
                )
                em.add_field(name="Before:", value=before.nick)
                em.add_field(name="After:", value=after.nick)
                async with aiosqlite.connect("databases/log.db") as con:
                    cur = await con.execute(
                        "SELECT * FROM log WHERE GuildID=?", (before.guild.id,)
                    )
                    data = await cur.fetchone()
                if data:
                    if data[2] == 0 and before.bot:
                        return
                    channel = self.client.get_channel(data[1])
                    await channel.send(embed=em)
                    return

            if before.roles != after.roles:
                if len(before.roles) > len(after.roles):
                    em = discord.Embed(
                        color=discord.Color.red(),
                        title="Role removed",
                        description=f"{before.name} Has lost a role",
                        timestamp=datetime.datetime.utcnow(),
                    )
                    for i in before.roles:
                        if i not in after.roles:
                            em.add_field(name="Role:", value=i.name)
                            em.set_thumbnail(url=before.avatar.url)
                            async with aiosqlite.connect("databases/log.db") as con:
                                cur = await con.execute(
                                    "SELECT * FROM log WHERE GuildID=?",
                                    (before.guild.id,),
                                )
                                data = await cur.fetchone()
                            if data:
                                channel = self.client.get_channel(data[1])
                                await channel.send(embed=em)
                                return

                elif len(before.roles) < len(after.roles):
                    em = discord.Embed(
                        color=discord.Color.green(),
                        title="Role added",
                        description=f"{before.name} Has gained a role",
                        timestamp=datetime.datetime.utcnow(),
                    )
                    for i in after.roles:
                        if i not in before.roles:
                            em.add_field(name="Role:", value=i.name)
                            em.set_thumbnail(url=after.avatar.url)
                            async with aiosqlite.connect("databases/log.db") as con:
                                cur = await con.execute(
                                    "SELECT * FROM log WHERE GuildID=?",
                                    (before.guild.id,),
                                )
                                data = await cur.fetchone()
                            if data:
                                channel = self.client.get_channel(data[1])
                                await channel.send(embed=em)
                                return
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        em = discord.Embed(
            color=discord.Color.blue(),
            title="Member Banned!",
            description=f"{user.name} Has been banned from the server",
            timestamp=datetime.datetime.utcnow(),
        )
        async with aiosqlite.connect("databases/log.db") as con:
            cur = await con.execute("SELECT * FROM log WHERE GuildID=?", (guild.id,))
            data = await cur.fetchone()
        if data:
            try:
                channel = self.client.get_channel(data[1])
                await channel.send(embed=em)
            except Exception:
                pass
        else:
            return

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        em = discord.Embed(
            color=discord.Color.blue(),
            title="Member Unbanned!",
            description=f"{user.name} Has been unbanned from the server",
            timestamp=datetime.datetime.utcnow(),
        )
        async with aiosqlite.connect("databases/log.db") as con:
            cur = await con.execute("SELECT * FROM log WHERE GuildID=?", (guild.id,))
            data = await cur.fetchone()
        if data:
            try:
                channel = self.client.get_channel(data[1])
                await channel.send(embed=em)
            except Exception:
                pass
        else:
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        em = discord.Embed(
            color=discord.Color.red(),
            title="Channel deleted!",
            description=f"{channel.name} Has been deleated from the server",
            timestamp=datetime.datetime.utcnow(),
        )
        em.add_field(name="Channel:", value=channel.name, inline=False)
        async with aiosqlite.connect("databases/log.db") as con:
            cur = await con.execute(
                "SELECT * FROM log WHERE GuildID=?", (channel.guild.id,)
            )
            data = await cur.fetchone()
        if data:
            channel = self.client.get_channel(data[1])
            await channel.send(embed=em)
        else:
            return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        em = discord.Embed(
            color=discord.Color.green(),
            title="Channel created!",
            description=f"{channel.name} Has been created in the server",
            timestamp=datetime.datetime.utcnow(),
        )
        em.add_field(name="Channel:", value=channel.name)
        con = sqlite3.connect("databases/log.db")
        cur = con.cursor()
        async with aiosqlite.connect("databases/log.db") as con:
            cur = await con.execute(
                "SELECT * FROM log WHERE GuildID=?", (channel.guild.id,)
            )
            data = await cur.fetchone()
        if data:
            channel = self.client.get_channel(data[1])
            await channel.send(embed=em)
        else:
            return

    # on message delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.client.user.id:
            return

        em = discord.Embed(
            color=discord.Color.red(),
            title="Message Deleted",
            description=f"{message.author} message was deleted",
        )
        em.add_field(name="Message", value=message.content, inline=False)
        em.add_field(name="Channel", value=message.channel, inline=False)
        em.add_field(
            name="Link",
            value=f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
            inline=False,
        )
        em.add_field(name="Time", value=message.created_at)

        # if there is a attachment
        if message.attachments:
            em.add_field(name="Attachment", value=message.attachments[0].url)

        async with aiosqlite.connect("databases/log.db") as con:
            async with con.execute(
                "SELECT * FROM log WHERE GuildID=?", (message.guild.id,)
            ) as cur:
                data = await cur.fetchone()
                if data:
                    try:
                        channel = self.client.get_channel(data[1])
                        await channel.send(embed=em)
                    except Exception:
                        pass
                else:
                    return


def setup(client):
    client.add_cog(Moderationsettings(client))
