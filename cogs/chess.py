import discord
from datetime import datetime
from time import sleep
import requests
from discord.ext import commands


class chess(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command(aliases=['coft'])
    async def TodaysChess(self, ctx):
        url = 'https://api.chess.com/pub/puzzle/random'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"{data['title']}", color=0x20BEFF)
        embed.set_image(url=data['image'])
        embed.add_field(name="fen:", value=data['fen'], inline=False)
        embed.add_field(name="url:", value=data['url'], inline=False)
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(chess(client))
