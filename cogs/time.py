import time
import calendar
import discord
from discord.ext import commands


class Time(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command(name='time', help="Get the current time and shows it in a human readable format. in the readers time zone")
    async def time(self, ctx):
        t = int(time.time())
        await ctx.send(f"The time is <t:{t}>")

    @commands.command(name='date', help="Get the current date and shows it in a human readable format. in the readers time zone")
    async def fdate(self, ctx , * ,message):
        t = calendar.timegm(time.strptime(message, '%Y-%m-%d'))
        await ctx.send(f"The time and date will be <t:{t}:D>")

    @commands.command( help="Get the current date and shows it in a human readable format. in the readers time zone")
    async def ftime(self, ctx , * ,message):
        t = calendar.timegm(time.strptime(message, '%H:%M'))
        await ctx.send(f"The time and date will be <t:{t}:t>")

    @commands.command(name='timezone', help="Get the current time and shows it in a human readable format. in the readers time zone")
    async def timezone(self, ctx, *, message):
        t = calendar.timegm(time.strptime(message, '%Y-%m-%d %H:%M'))
        await ctx.send(f"The time and date will be <t:{t}>")

def setup(client):
    client.add_cog(Time(client))
