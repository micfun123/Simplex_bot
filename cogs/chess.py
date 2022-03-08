import discord
from datetime import datetime
from time import sleep
import requests
from discord.ext import commands
from discord.commands import slash_command


class chess(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command(name = "todayschess", help = "Gets you todays chess challenge",)
    async def todaysChess_(self, ctx):
        url = 'https://chesspuzzle.net/Daily/Api'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['Puzzle']}", color=0x20BEFF)
        embed.set_image(url=data['Image'])
        embed.add_field(name="To Start:", value=data['Text'], inline=False)
        embed.add_field(name="url:", value=data['Link'], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)


    @slash_command(name = "todayschess", help = "Gets you todays chess challenge")
    async def todaysChess(self, ctx):
        url = 'https://chesspuzzle.net/Daily/Api'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['Puzzle']}", color=0x20BEFF)
        embed.set_image(url=data['Image'])
        embed.add_field(name="To Start:", value=data['Text'], inline=False)
        embed.add_field(name="url:", value=data['Link'], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(chess(client))
