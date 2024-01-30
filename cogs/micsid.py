import logging

import imp
import discord
from discord.ext import commands
import json
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import subprocess
from discordLevelingSystem import DiscordLevelingSystem
import aiosqlite

DISCORD_LOG_PATH = "other/discord.log"


def add_logger():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(filename=DISCORD_LOG_PATH, encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    logger.addHandler(handler)


def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("./other/log.txt", "a") as f:
        f.write("\n")
        f.write(f"{timern} | {log}")


cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])


class BotMakerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        add_logger()

    @commands.command()
    @commands.check(micsid)
    async def logs(self, ctx):
        file = discord.File("./other/log.txt")
        await ctx.author.send(file=file)

    @commands.command()
    @commands.check(micsid)
    async def discord_logs(self, ctx):
        file = discord.File(DISCORD_LOG_PATH)
        await ctx.author.send(file=file)

    @commands.command()
    @commands.check(micsid)
    async def msgserver(self, ctx, id: int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")

    @commands.command()
    @commands.check(micsid)
    async def reloadall(self, ctx):
        lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
        no_py = [s.replace(".py", "") for s in lst]
        startup_extensions = ["cogs." + no_py for no_py in no_py]
        startup_extensions.remove("cogs.Leveling")

        try:
            for cogs in startup_extensions:
                self.client.reload_extension(cogs)

            await ctx.send("All Reloaded")

        except Exception as e:
            print(e)
            log(e)

    @commands.command(hidden=True)
    @commands.check(micsid)
    async def pull(self, ctx):
        gitstuff = subprocess.run(["git", "pull"], capture_output=True).stdout
        await ctx.send(gitstuff.decode())
        log(gitstuff.decode())

    @commands.command(help="Dms all server owners")
    @commands.check(micsid)
    async def dm_owners(self, ctx, *, msg):
        await ctx.send("Sending...")
        log(f"DMing all owners with {msg}")
        mins = 0
        # predicts how long it will take
        mins = len(self.client.guilds) * 0.1
        await ctx.send(f"Estimated time: {mins} minutes")

        owners = []
        for server in self.client.guilds:
            tosend = server.owner
            owners.append(tosend)
        owners = list(set(owners))
        for i in owners:
            try:
                await i.send(msg)
            except:
                await ctx.send(f"Counld not send to {i}")
        await ctx.send("Done")

    @commands.command()
    @commands.check(micsid)
    async def ghoastping(self, ctx, *, member: discord.Member):
        for i in ctx.guild.channels:
            try:
                x = await i.send(f"{member.mention}")
                await x.delete()
            except:
                print(f"Can't send message in {i}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clearlog(self, ctx):
        file = discord.File("./other/log.txt")
        await ctx.author.send(file=file)
        dirs = "other/"
        for f in os.listdir(dirs):
            os.remove(os.path.join(dirs, f))
        dirs = "tempstorage/"
        for f in os.listdir(dirs):
            os.remove(os.path.join(dirs, f))
        await ctx.send("Cleared")
        await log("Cleared at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    @commands.command(hidden=True)
    @commands.check(micsid)
    async def status(self, ctx):
        gitstuff = subprocess.run(["git", "status"], capture_output=True).stdout
        await ctx.send(gitstuff.decode())
        log(gitstuff.decode())

    @commands.command()
    @commands.check(micsid)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Load", description=f"{extension} successfully loaded", color=0xFF00C8
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(micsid)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"The module '{extension}' has been unloaded successfully!")

    @commands.command()
    @commands.is_owner()
    async def change_status(self, ctx, *, status):
        status = status.replace("[[servers]]", str(len(self.client.guilds)))
        await self.client.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Status changed to {status}")

    @commands.command()
    @commands.is_owner()
    async def commandlookup(self, ctx, command):
        # check if command exists
        if self.client.get_command(command) == None:
            await ctx.send("Command not found")
            return
        # find the cog
        for i in self.client.cogs:
            if (
                self.client.get_command(command)
                in self.client.get_cog(i).get_commands()
            ):
                cog = i
        await ctx.send(f"Cog: {cog}\nCommand: {command}")

    # when a command is used, it will be logged
    @commands.Cog.listener()
    async def on_command(self, ctx):
        # check if file exists
        if os.path.isfile(f"databases/command_usage.db"):
            async with aiosqlite.connect("databases/command_usage.db") as db:
                # check if command is in database
                async with db.execute(
                    "SELECT * FROM command_usage WHERE command = ?", (ctx.command.name,)
                ) as cursor:
                    data = await cursor.fetchall()
                    # if command is not in database
                    if len(data) == 0:
                        await db.execute(
                            "INSERT INTO command_usage VALUES (?, ?, ?)",
                            (
                                ctx.command.name,
                                1,
                                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            ),
                        )
                        await db.commit()
                    # if command is in database
                    else:
                        await db.execute(
                            "UPDATE command_usage SET times_used = ?, last_used = ? WHERE command = ?",
                            (
                                data[0][1] + 1,
                                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                ctx.command.name,
                            ),
                        )
                        await db.commit()

        else:
            async with aiosqlite.connect("databases/command_usage.db") as db:
                await db.execute(
                    "CREATE TABLE command_usage (command TEXT, times_used INTEGER, last_used TEXT)"
                )
                await db.commit()

    @commands.command()
    @commands.check(micsid)
    async def commandusage(self, ctx, command):
        if os.path.isfile(f"databases/command_usage.db"):
            async with aiosqlite.connect("databases/command_usage.db") as db:
                async with db.execute(
                    "SELECT * FROM command_usage WHERE command = ?", (command,)
                ) as cursor:
                    data = await cursor.fetchall()
                    if len(data) == 0:
                        await ctx.send("Command not found")
                    else:
                        embed = discord.Embed(
                            title="Command Usage",
                            description=f"Command: {data[0][0]}\nTimes used: {data[0][1]}\nLast used: {data[0][2]}",
                            color=0xFF00C8,
                        )
                        await ctx.send(embed=embed)
        else:
            await ctx.send("Command not found")

    @commands.command()
    @commands.check(micsid)
    async def commandusagelist(self, ctx):
        if os.path.isfile(f"databases/command_usage.db"):
            async with aiosqlite.connect("databases/command_usage.db") as db:
                async with db.execute("SELECT * FROM command_usage") as cursor:
                    data = await cursor.fetchall()
                    if len(data) == 0:
                        await ctx.send("No commands found")
                    else:
                        embed = discord.Embed(
                            title="Command Usage",
                            description="Command: Times used: Last used:",
                            color=0xFF00C8,
                        )
                        for i in data:
                            embed.description += f"\n{i[0]}: {i[1]}: {i[2]}"
                        await ctx.send(embed=embed)
        else:
            await ctx.send("No commands found")

    @commands.command()
    @commands.is_owner()
    async def server_invite(self, ctx, *, server):
        guild = self.client.get_guild(int(server))
        if guild == None:
            await ctx.send("Server not found")
            return
        invite = await guild.channels[0].create_invite()
        await ctx.send(invite)

    @commands.command()
    @commands.is_owner()
    async def server_look_up(self, ctx, *, server):
        guild = self.client.get_guild(int(server))
        if guild == None:
            await ctx.send("Server not found")
            return
        embed = discord.Embed(
            title=guild.name, description=f"ID: {guild.id}", color=0xFF00C8
        )
        embed.add_field(
            name="Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}"
        )
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(
            name="Created at", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        )
        embed.add_field(name="Owner ID", value=guild.owner.id)

        try:
            embed.set_thumbnail(url=guild.icon.url)
        except:
            pass

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(BotMakerCommands(client))
