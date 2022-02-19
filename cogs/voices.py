import imp
import aiofiles
import discord
from discord.ext import commands
import aiohttp
import os
import requests


class funtranslations(commands.Cog):
    def __init__(self, client): 
        self.client = client 

    @commands.command(help="yoda speak")
    async def yoda(self, ctx, *, text):
        send = text.replace(" ", "%20")
        url = f"https://api.funtranslations.com/translate/yoda.json?text={send}"
        response = requests.get(url)
        data = response.json()
        await ctx.send(data["contents"]["translated"])

    @commands.command(help="pirate speak")
    async def pirate(self, ctx, *, text):
        send = text.replace(" ", "%20")
        url = f"https://api.funtranslations.com/translate/pirate.json?text={send}"
        response = requests.get(url)
        data = response.json()
        await ctx.send(data["contents"]["translated"])

    
def setup(client):
    client.add_cog(funtranslations(client))
    
