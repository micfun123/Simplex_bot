from discord.ext import commands, tasks
import discord
import asyncio
import os
import json
import sqlite3
from datetime import datetime,time

class Birthday(commands.Cog):
    """Birthday commands."""

    def __init__(self, client):
        self.client = client
        self.birthdaytimer.start()

    @commands.command(hidden = True)
    @commands.is_owner()
    async def force_add_user(self, ctx, user: discord.Member, day: int, month: int):
        """Adds a user to the birthday list."""
        if day > 31 or day < 1 or month > 12 or month < 1:
            await ctx.send("Invalid date.")
            return
        con = sqlite3.connect("databases/user_brithdays.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM birthday WHERE user_id = ?", (user.id,))
        if cur.fetchone() is not None:
            await ctx.send("User already exists.")
            return
        cur.execute("INSERT INTO birthday VALUES (?, ?, ?)", (user.id, day, month))
        con.commit()
        con.close()
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def makeservertablebirthday(self,ctx):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE server(ServerID int, Servertoggle, birthdaychannel int)")
        con.commit()
        con.close()
        con = sqlite3.connect("databases/user_brithdays.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE birthday(UsersID int, birthday)")
        con.commit()
        con.close()
        await ctx.send("Done")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def setallbithday(self,ctx):
        for i in self.client.guilds:
            con = sqlite3.connect("databases/server_brithdays.db")
            cur = con.cursor()
            cur.execute("INSERT INTO server(ServerID, Servertoggle,birthdaychannel) VALUES(?, ?,?)", (i.id, False,None))
            await ctx.send(f"{i} has been set")
            con.commit()
            con.close()
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        

        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("INSERT INTO server(ServerID, Servertoggle) VALUES(?, ?)", (guild.id, False))
        con.commit()
        con.close()

    @commands.command(help = " enable and disable Birthday")
    @commands.has_permissions(administrator=True)
    async def toggle_birthday(self,ctx):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        datas = cur.execute("SELECT * FROM server WHERE ServerID=?", (ctx.guild.id,))
        datas = cur.fetchall()
        toggle = datas[0][1]
        if toggle == True:
            cur.execute("UPDATE server SET Servertoggle = ? WHERE ServerID=?", (False, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.send("Birthday reminders has been turned off")
        if toggle == False:
            cur.execute("UPDATE server SET Servertoggle = ? WHERE ServerID=?", (True, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.send("Birthday reminders has been turrned on")

    @commands.slash_command(name="setbirthday", description="Set your birthday use day then month")
    async def setbirthday__slash(self, ctx, day: int, month: int):
        if day > 31 or day < 1 or month > 12 or month < 1:
            await ctx.respond("Invalid date.")
        else:
            con = sqlite3.connect("databases/user_brithdays.db")
            cur = con.cursor()
            data = cur.execute("SELECT * FROM birthday WHERE UsersID=?", (ctx.author.id,))
            data = cur.fetchall()
            if data == []:
                cur.execute("INSERT INTO birthday(UsersID, birthday) VALUES(?, ?)", (ctx.author.id, f"{day}/{month}"))
                con.commit()
                con.close()
                await ctx.respond("Your birthday has been set")
            else:
                cur.execute("UPDATE birthday SET birthday = ? WHERE UsersID=?", (f"{day}/{month}", ctx.author.id,))
                con.commit()
                con.close()
                await ctx.respond("Your birthday has been updated")
        
    @commands.command(name="setbirthday", help = "Set your birthday use day then month")
    async def setbirthday_commands(self, ctx, day: int, month: int):
        if day > 31 or day < 1 or month > 12 or month < 1:
            await ctx.send("Invalid date.")
        else:
            con = sqlite3.connect("databases/user_brithdays.db")
            cur = con.cursor()
            data = cur.execute("SELECT * FROM birthday WHERE UsersID=?", (ctx.author.id,))
            data = cur.fetchall()
            if data == []:
                cur.execute("INSERT INTO birthday(UsersID, birthday) VALUES(?, ?)", (ctx.author.id, f"{day}/{month}"))
                con.commit()
                con.close()
                await ctx.send("Your birthday has been set")
            else:
                cur.execute("UPDATE birthday SET birthday = ? WHERE UsersID=?", (f"{day}/{month}", ctx.author.id,))
                con.commit()
                con.close()
                await ctx.send("Your birthday has been updated")

    @commands.command(help = "Set the birthday channel")
    @commands.has_permissions(administrator=True)
    async def set_birthday_channel(self,ctx, channel: commands.TextChannelConverter):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("UPDATE server SET birthdaychannel = ? WHERE ServerID=?", (channel.id, ctx.guild.id,))
        con.commit()
        con.close()
        await ctx.send(f"Birthday channel has been set to {channel}")

    #runs every 24 hours
    @tasks.loop(time=time(12,00))
    async def birthdaytimer(self):
        await self.client.wait_until_ready()
        for i in self.client.guilds:
            con = sqlite3.connect("databases/server_brithdays.db")
            cur = con.cursor()
            datas = cur.execute("SELECT * FROM server WHERE ServerID=?", (i.id,))
            datas = cur.fetchall()
            toggle = datas[0][1]
            channel = datas[0][2]
            con.close()
            if toggle == True:
                con = sqlite3.connect("databases/user_brithdays.db")
                cur = con.cursor()
                data = cur.execute("SELECT * FROM birthday")
                data = cur.fetchall()
                for i in data:
                    if i[1] == datetime.now().strftime("%d/%m"):
                        channel = self.client.get_channel(channel)
                        await channel.send(f"<@{i[0]}> Happy Birthday")
                con.close()
            else:
                pass




            

        
        
        




def setup(bot):
    bot.add_cog(Birthday(bot))


