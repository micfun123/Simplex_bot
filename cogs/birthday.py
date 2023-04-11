from discord.ext import commands, tasks
import discord
import asyncio
import os
import json
import sqlite3
from dotenv import load_dotenv
import requests
from datetime import datetime,time

load_dotenv()

class Birthday(commands.Cog):
    """Birthday commands."""

    def __init__(self, client):
        self.client = client
        self.birthday_announcments.start()


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
        await ctx.send("Added user to birthday list.")
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def makeservertablebirthday(self,ctx):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE server(ServerID int, Servertoggle, birthdaychannel int,birthdaymessage text)")
        con.commit()
        con.close()
        con = sqlite3.connect("databases/user_brithdays.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE birthday(UsersID int, birthday)")
        con.commit()
        con.close()
        await ctx.send("Done")
#
    #@commands.command(hidden = True)
    #@commands.is_owner()
    #async def setallbithday(self,ctx):
    #    for i in self.client.guilds:
    #        con = sqlite3.connect("databases/server_brithdays.db")
    #        cur = con.cursor()
    #        cur.execute("INSERT INTO server(ServerID, Servertoggle,birthdaychannel) VALUES(?, ?,?)", (i.id, False,None))
    #        await ctx.send(f"{i} has been set")
    #        con.commit()
    #        con.close()
        
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
    
    @commands.slash_command(name="toggle_birthday", description="enable and disable Birthday")
    @commands.has_permissions(administrator=True)
    async def _toggle_birthday(self,ctx):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        datas = cur.execute("SELECT * FROM server WHERE ServerID=?", (ctx.guild.id,))
        datas = cur.fetchall()
        toggle = datas[0][1]
        if toggle == True:
            cur.execute("UPDATE server SET Servertoggle = ? WHERE ServerID=?", (False, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.respond("Birthday reminders has been turned off")
        if toggle == False:
            cur.execute("UPDATE server SET Servertoggle = ? WHERE ServerID=?", (True, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.respond("Birthday reminders has been turrned on")
        await ctx.followup.send("If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D", ephemeral=True)


    @commands.slash_command(name="setbirthday", description="Set your birthday use day then month")
    async def setbirthday__slash(self, ctx, day: int, month: int):
        tocken = os.getenv("TOPGG_TOKEN")
        api = requests.get(f"https://top.gg/api/bots/902240397273743361/check?userId={ctx.author.id}", headers={"Authorization": tocken, "Content-Type": "application/json"})
        data = api.json()
        print(api)
        print(data)
        voted = data["voted"]
        #if the api does not return a 200 status code
        if api.status_code != 200:
            voted = 1
            print("api error")
        if voted == 0:
            await ctx.respond("You need to have voted for simplex in the last 24 hours to set your birthday. Please vote and then try again, you can vote here: https://top.gg/bot/902240397273743361/vote")
            return
        else:
            if day > 31 or day < 1 or month > 12 or month < 1:
                await ctx.respond("Invalid date.")
            else:
                #force 2 digit date
                if day < 10:
                    day = f"0{day}"
                if month < 10:
                    month = f"0{month}"

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
            #formate date 2 digit
            if len(str(day)) == 1:
                day = f"0{day}"
            if len(str(month)) == 1:
                month = f"0{month}"


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

    @commands.command(name="set_birthday_channel",help = "Set the birthday channel")
    @commands.has_permissions(administrator=True)
    async def set_birthday_channel_command(self,ctx, channel: commands.TextChannelConverter):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("UPDATE server SET birthdaychannel = ? WHERE ServerID=?", (channel.id, ctx.guild.id,))
        con.commit()
        con.close()
        await ctx.send(f"Birthday channel has been set to {channel}")

    @commands.slash_command(name="set_birthday_channel",help = "Set the birthday channel")
    @commands.has_permissions(administrator=True)
    async def set_birthday_channel__slash(self,ctx, channel: commands.TextChannelConverter):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        cur.execute("UPDATE server SET birthdaychannel = ? WHERE ServerID=?", (channel.id, ctx.guild.id,))
        con.commit()
        con.close()
        await ctx.respond(f"Birthday channel has been set to {channel}")


    @commands.slash_command(name="findbirthday", description="Find a users birthday")
    async def findbirthday__slash(self, ctx, user: discord.Member):
        con = sqlite3.connect("databases/user_brithdays.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM birthday WHERE UsersID=?", (user.id,))
        data = cur.fetchall()
        if data == []:
            await ctx.respond(f"{user} has not set their birthday")
        else:
            await ctx.respond(f"{user} birthday is {data[0][1]}")
        await ctx.followup.send("If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D", ephemeral=True)


    @tasks.loop(time=time(7,00))
    async def birthday_announcments(self):
        print("Birthday announcments")
        for server in self.client.guilds:
                print(server)
                con = sqlite3.connect("databases/server_brithdays.db")
                cur = con.cursor()
                datas = cur.execute("SELECT * FROM server WHERE ServerID=?", (server.id,))
                datas = cur.fetchall()
                if datas == []:
                    cur.execute("INSERT INTO server(ServerID, Servertoggle, birthdaychannel) VALUES(?, ?, ?)", (server.id, False, None))
                    con.commit()
                    con.close()
                else:
                    pass
                con = sqlite3.connect("databases/user_brithdays.db")
                cur = con.cursor()
                data = cur.execute("SELECT * FROM birthday")
                data = cur.fetchall()
                if data == []:
                    print("No birthday")
                    #does not work below here
                else:
                    for x in data:
                        if datas[0][1] == True:
                            if datas[0][2] == None:
                                pass
                            else:
                                user = await self.client.fetch_user(x[0])
                                if user in server.members:
                                    channel = await self.client.fetch_channel(datas[0][2])
                                    message = datas[0][3]
                                    if message == None:
                                        message = ":tada:"

                                    print(channel)
                                    print(x[1])
                                    print(datetime.now().strftime("%d/%m"))
                                    if x[1] == datetime.now().strftime("%d/%m"):
                                        print("Birthday")
                                        print(x[0])
                                        await channel.send(f"Happy birthday <@{x[0]}>! \n {message}")
                                else:
                                    username = await self.client.fetch_user(x[0])
                                    print(f"User {username} not in server {x[0]} {server}")
                        else:
                            pass

        
    #@commands.command()
    #@commands.is_owner()
    #async def foramt_all_birthdays(self,ctx):
    #    con = sqlite3.connect("databases/user_brithdays.db")
    #    cur = con.cursor()
    #    data = cur.execute("SELECT * FROM birthday")
    #    data = cur.fetchall()
    #    for i in data:
    #        day = i[1].split("/")[0]
    #        month = i[1].split("/")[1]
    #        if len(day) == 1:
    #            day = "0" + day
    #        if len(month) == 1:
    #            month = "0" + month
    #        cur.execute("UPDATE birthday SET Birthday = ? WHERE UsersID=?", (f"{day}/{month}", i[0],))
    #        con.commit()
    #    con.close()
    #    

    @commands.command()
    @commands.is_owner()
    async def add_message_to_birthday(self,ctx,*,message):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        #creat a new column
        cur.execute("ALTER TABLE server ADD COLUMN birthdaymessage TEXT")
        #set the message
        cur.execute("UPDATE server SET birthdaymessage = ?", (message,))
        con.commit()
        con.close()
        await ctx.send("Done")

    @commands.slash_command(name="birthday_message", description="Add a message to the birthday announcment")
    @commands.has_permissions(administrator=True)
    async def add_message_to_birthday__slash(self,ctx,*,message):
        con = sqlite3.connect("databases/server_brithdays.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM server WHERE ServerID=?", (ctx.guild.id,))
        data = cur.fetchall()
        if data == []:
            await ctx.respond("You have not set a birthday channel")
        else:
            cur.execute("UPDATE server SET birthdaymessage = ? WHERE ServerID=?", (message, ctx.guild.id,))
            con.commit()
            con.close()
            await ctx.respond("Done")
            await ctx.followup.send("If you like the bot, please consider voting for it at https://top.gg/bot/902240397273743361 \n It helps a lot! :D", ephemeral=True)


def setup(bot):
    bot.add_cog(Birthday(bot))


