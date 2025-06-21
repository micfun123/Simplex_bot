import discord
from datetime import datetime
from time import sleep
import requests
from discord.ext import commands
from discord.commands import slash_command


class cards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="randomcard", help="Gets you a random card")
    async def randomcard_(self, ctx):
        url = "https://deckofcardsapi.com/api/deck/new/draw/?count=1"
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"Random Card", color=0x20BEFF)
        embed.description = f"{data['cards'][0]['value']} of {data['cards'][0]['suit']}"
        embed.set_image(url=data["cards"][0]["image"])
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.send(embed=embed)

    @slash_command(name="randomcard", help="Gets you a random card")
    async def randomcard(self, ctx):
        url = "https://deckofcardsapi.com/api/deck/new/draw/?count=1"
        response = requests.get(url)
        data = response.json()
        embed = discord.Embed(title=f"Random Card", color=0x20BEFF)
        embed.description = f"{data['cards'][0]['value']} of {data['cards'][0]['suit']}"
        embed.set_image(url=data["cards"][0]["image"])
        embed.set_footer(text="Time: " + str(datetime.now()))
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(cards(client))
