import imp
from datetime import timedelta 
import datetime
from datetime import datetime
import discord
from discord.ext import commands
import asyncio
import time
import os
import psutil
import requests

def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        if i.endswith(".py"):
            files.append(f"cogs/{i}")
    for i in files:
        count = 0
        with open(i, 'r',encoding="utf8") as f:
            for line in f:
                count += 1
        lines += count
    return lines

class utilities(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    

    @commands.command(aliases=['sug', 'suggestion'])
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(908969607266730005)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.command()
    async def serverinfo(self,ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)


        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Created: ", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>", inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)


    #gets user info of user on the discord
    @commands.command(aliases=["userinfo", "ui"] ,help = "Finds info about users on the discord.")
    async def info(self,ctx, user: discord.Member):
        embed = discord.Embed(title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00ff00)
        embed.add_field(name="Username:", value=user.name, inline=True)
        embed.add_field(name="ID:", value=user.id, inline=True)
        embed.add_field(name="Status:", value=user.status, inline=True)
        embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
        embed.add_field(name="Joined Server:", value=user.joined_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"), inline=True)
        embed.add_field(name="Created Account:", value=user.created_at.strftime("%a, %#d, %B, %Y, #I:%M %p UTC"), inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["channel_stats", "channel_health", "channel_info", "channel_information"])
    async def channel_status(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        server_id = self.client.get_guild(self.client.guilds[0].id)

        embed = discord.Embed(colour=discord.Colour.orange())
        embed.set_author(name="Channel Health:")

        async with ctx.channel.typing():
            count = 0
            async for message in channel.history(limit=500000, after=datetime.today() - timedelta(days=100)): count += 1

            if count >= 5000:
                average = "OVER 5000!"
                healthiness = "VERY HEALTHY"

            else:
                try:
                    average = round(count / 100, 2)

                    if 0 > server_id.member_count / average: healthiness = "VERY HEALTHY"
                    elif server_id.member_count / average <= 5: healthiness = "HEALTHY"
                    elif server_id.member_count / average <= 10: healthiness = "NORMAL"
                    elif server_id.member_count / average <= 20: healthiness = "UNHEALTHY"
                    else: healthiness = "VERY UNHEALTHY"

                except ZeroDivisionError:
                    average = 0
                    healthiness = "VERY UNHEALTHY"

            embed.add_field(name="­", value=f"# of members: {server_id.member_count}", inline=False)
            embed.add_field(name="­", value=f'# of messages per day on average in "{channel}" is: {average}', inline=False)
            embed.add_field(name="­", value=f"Channel health: {healthiness}", inline=False)

            await ctx.send(embed=embed)


    @commands.command()
    async def botinfo(self, ctx):
        em = discord.Embed(title = 'Simplex')
        em.add_field(inline = False,name="Server Count", value=f"{len(self.client.guilds)}")
        mlist = []
        for i in list(self.client.get_all_members()):
            mlist.append(i.name)
        em.add_field(inline = False,name="User Count", value=len(mlist))
        em.add_field(inline = False,name="Active users", value=f"{len(set(mlist))}")
        em.add_field(inline = False,name="Ping", value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Made by the Simplex Dev Team")
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline = False)
        em.add_field(name="Python code", value=f"{get_lines()} of code",inline = False)
        em.add_field(name="Commands", value=f"{len(self.client.commands)} of commands")

        await ctx.send(embed = em)

    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.send(embed=message)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self} has been loaded') 
        global startTime 
        startTime = time.time()

    @commands.command(name='Uptime')
    async def _uptime(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        e = discord.Embed(title="Uptime", description=uptime, color=0x8BE002)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(utilities(bot))