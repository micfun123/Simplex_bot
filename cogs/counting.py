import discord
import discord
from discord.ext import commands
import json
from simpcalc import simpcalc
import asyncio
import sqlite3


calculator = simpcalc.Calculate()

# Counting


async def counting(msg, guild, channel, m):
    try:
      calc = simpcalc.Calculate()
      ans = await calc.calculate(msg)
      msg = int(ans)
    except:
     return    
    con = sqlite3.connect("databases/counting.db")
    cur = con.cursor()
    ##get counting channel
    countingchannel = cur.execute("SELECT counting_channel FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
    if countingchannel is None:
        return
    if countingchannel != channel.id:
        return
    else:
        ##get last number
        lastnumber = cur.execute("SELECT lastcounter FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
        lastuser = cur.execute("SELECT last_user FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
        highest = cur.execute("SELECT highest FROM counting WHERE Guild_id = ?", (guild.id,)).fetchone()[0]
        if lastnumber is None:
            cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
            con.commit()
            con.close()
            return
        if msg == lastnumber + 1:
            if lastuser == m.author.id:
                await m.add_reaction("❌")
                em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description="Take it in turns and stop being selfish\nCount reset to zero")
                cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
                cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
                con.commit()
                con.close()
                return await channel.send(embed=em)
            else:
                
                cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (msg, guild.id))
                cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (m.author.id, guild.id))
                if msg == highest+1:
                    cur.execute("UPDATE counting SET highest = ? WHERE Guild_id = ?", (msg, guild.id))
                    await m.add_reaction("☑")
                else:
                    await m.add_reaction("✅")
                con.commit()
                con.close()
                if msg == 69:
                    await channel.send("nice")
                if msg == 420:
                    await channel.send("nice")
                if msg == 42069:
                    await channel.send("You have found the meaning of life.")
                return
        else:
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.display_name}, You ruined it!", description=f"Count reset to zero. you were supposed to count {lastnumber + 1}")
            cur.execute("UPDATE counting SET lastcounter = ? WHERE Guild_id = ?", (0, guild.id))
            cur.execute("UPDATE counting SET last_user = ? WHERE Guild_id = ?", (None, guild.id))
            con.commit()
            con.close()
            return await channel.send(embed=em)

class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.command()
    async def makedbtable(self, ctx):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE counting (guild_id INTEGER, counting_channel INTEGER, lastcounter INTEGER,highest INTEGER, last_user INTEGER)")
        con.commit()
        for i in self.client.guilds:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?,?)", (i.id, None, None, 0, None))
        con.commit()
        con.close()
        await ctx.send("Done")


    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)

    def mic(ctx):
        return ctx.author.id == 481377376475938826

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_num(self,ctx,nums):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM counting WHERE guild_id = ?", (ctx.guild.id,))
        data = cur.fetchone()
        num = int(nums)
        cur.execute("UPDATE counting SET lastcounter = ? WHERE guild_id = ?", (nums, ctx.guild.id))
        con.commit()
        con.close()
        await ctx.send(f"Numb set to {nums}")
            
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcountchannel(self, ctx, channel:discord.TextChannel):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("UPDATE counting SET counting_channel = ? WHERE guild_id = ?", (channel.id, ctx.guild.id))
        con.commit()
        con.close()
        await ctx.send(f"Counting channel set to {channel.mention}")
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def countingoff(self, ctx):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        cur.execute("UPDATE counting SET counting_channel = ? WHERE guild_id = ?", (None, ctx.guild.id))
        con.commit()
        con.close()
        await ctx.send(f"Counting channel turned off")
    
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        con = sqlite3.connect("./databases/counting.db")
        cur = con.cursor()
        data =  cur.execute("SELECT * FROM counting WHERE guild_id = ?", (guild.id,)).fetchall()
        if not data:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?)", (guild.id, None, None, 0))
            con.commit()
        con.close()


def setup(client):
    client.add_cog(Counting(client))
