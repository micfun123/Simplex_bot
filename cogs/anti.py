    
from tools import mic, log
import json
from discord import Guild, Option
import discord
from discord.ext import commands
import discord.ui 
import calendar, datetime, time
import sqlite3


class Protection(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    @commands.is_owner()
    async def madetablerade(self,ctx):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE raids(ServerID int, Servertoggle, raiders int)")
        con.commit()
        con.close()

    @commands.command()
    @commands.is_owner()
    async def setallraid(self,ctx):
        for i in self.client.guilds:
            con = sqlite3.connect("databases/raids.db")
            cur = con.cursor()
            cur.execute("INSERT INTO raids(ServerID, Servertoggle, raiders) VALUES(?, ?,?)", (i.id, False, 20))
            await ctx.send(f"{i} has been set")
            con.commit()
            con.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_raid_protections(self,ctx):
        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        datas = cur.execute("SELECT * FROM raids WHERE ServerID=?", (ctx.guild.id,))
        datas = cur.fetchall()
        toggle = datas[0][1]
        if toggle == True:
            cur.execute("UPDATE raids SET Servertoggle = ? WHERE ServerID=?", (False, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.send("Raid Protection has been turned off")
        if toggle == False:
            cur.execute("UPDATE raids SET Servertoggle = ? WHERE ServerID=?", (False, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.send("Raid Protection has been turrned on")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        

        con = sqlite3.connect("databases/raids.db")
        cur = con.cursor()
        cur.execute("INSERT INTO raids(ServerID, Servertoggle) VALUES(?, ?)", (guild.id, False))
        con.commit()
        con.close()
       



        




def setup(client):
    client.add_cog(Protection(client))


