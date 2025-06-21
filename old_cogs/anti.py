from tools import mic, log
import json
from discord import Guild, Option
import discord
from discord.ext import commands, tasks
import discord.ui
import calendar, datetime, time
import sqlite3

timer = time.time()


class Protection(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.resetraders.start()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def madetablerade(self, ctx):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE raids(ServerID int, Servertoggle, raiderneed int, currentrade int)"
        )
        con.commit()
        con.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setallraid(self, ctx):
        for i in self.client.guilds:
            con = sqlite3.connect("databases/raids.db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO raids(ServerID, Servertoggle, raiderneed, currentrade) VALUES(?, ?,?, ?)",
                (i.id, False, 20, 0),
            )
            await ctx.send(f"{i} has been set")
            con.commit()
            con.close()

    @commands.command(help=" enable and disable raid protection")
    @commands.has_permissions(administrator=True)
    async def toggle_raid_protections(self, ctx):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        datas = cur.execute("SELECT * FROM raids WHERE ServerID=?", (ctx.guild.id,))
        datas = cur.fetchall()
        toggle = datas[0][1]
        if toggle == True:
            cur.execute(
                "UPDATE raids SET Servertoggle = ? WHERE ServerID=?",
                (
                    False,
                    ctx.guild.id,
                ),
            )
            con.commit()
            con.close()
            await ctx.send("Raid Protection has been turned off")
        if toggle == False:
            cur.execute(
                "UPDATE raids SET Servertoggle = ? WHERE ServerID=?",
                (
                    True,
                    ctx.guild.id,
                ),
            )
            con.commit()
            con.close()
            await ctx.send("Raid Protection has been turrned on")

    @commands.command(help="The amount of users before raid protections starts")
    @commands.has_permissions(administrator=True)
    async def setraidnumb(self, ctx, raidnum):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute(
            "UPDATE raids SET raiderneed = ? WHERE ServerID=?",
            (
                raidnum,
                ctx.guild.id,
            ),
        )
        con.commit()
        con.close()
        await ctx.send(f"Numb has been changed to {raidnum}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO raids(ServerID, Servertoggle, raiderneed, currentrade) VALUES(?, ?,?, ?)",
            (guild.id, False, 20, 0),
        )
        con.commit()
        con.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global timer
        guild = member.guild.id
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        datas = cur.execute("SELECT * FROM raids WHERE ServerID=?", (member.guild.id,))
        datas = cur.fetchall()
        current = datas[0][3]
        if datas[0][1] == 1:
            if timer - time.time() <= 120.0:
                cur.execute(
                    "UPDATE raids SET currentrade = ? WHERE ServerID=?",
                    (
                        current + 1,
                        member.guild.id,
                    ),
                )
                con.commit()
                con.close()
            if timer - time.time() > 120:
                timer = time.time()
            if datas[0][2] <= datas[0][3]:
                await member.send(
                    f"you cannot join {member.guild} at the current due to a suspected raid please try again in 5 minutes"
                )
                owner = member.guild.owner
                await owner.send(
                    "There may be a raid curretly. the bot has temporarly stopped any one joining"
                )
                await member.kick(reason="IMAGINE RAIDING SKILL ISSUE")

    @tasks.loop(minutes=5)
    async def resetraders(self):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute("UPDATE raids SET currentrade = 0")
        con.commit()
        con.close()


def setup(client):
    client.add_cog(Protection(client))
