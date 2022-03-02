import discord
from datetime import datetime
from time import sleep
import requests
from discord.ext import commands


class cards(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command(aliases=['rc'])
    async def randomcard(self, ctx):
        url = 'https://deckofcardsapi.com/api/deck/new/draw/?count=1'
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"Random Card", color=0x20BEFF)
        embed.description = f"{data['cards'][0]['value']} of {data['cards'][0]['suit']}"
        embed.set_image(url=data['cards'][0]['image'])
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(cards(client))
