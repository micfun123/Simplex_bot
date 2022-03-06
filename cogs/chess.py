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
        url = 'https://api.chess.com/pub/puzzle/random'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['title']}", color=0x20BEFF)
        embed.set_image(url=data['image'])
        embed.add_field(name="fen:", value=data['fen'], inline=False)
        embed.add_field(name="url:", value=data['url'], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)


    @slash_command(name = "todayschess", help = "Gets you todays chess challenge")
    async def todaysChess(self, ctx):
        url = 'https://api.chess.com/pub/puzzle/random'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['title']}", color=0x20BEFF)
        embed.set_image(url=data['image'])
        embed.add_field(name="fen:", value=data['fen'], inline=False)
        embed.add_field(name="url:", value=data['url'], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(chess(client))
