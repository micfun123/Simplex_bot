import imp
from pydoc import describe
from discord import Embed
import wikipedia
from discord.ext import commands
import json
import os
import discord
import imp
from tools import log


class lookup(commands.Cog):
    def __init__(self, client): 
        self.client = client 




    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx, *, query):
        embed = Embed(title="Wikipedia", description="Searching for {}".format(query), color=0x00ff00)
        page = wikipedia.summary(query, sentences=500)
        url = wikipedia.page(query).url
        embed.description = page
        embed.add_field(name="Link", value=url ,inline=False)
        await ctx.send(embed=embed)
       
    @commands.command()
    async def wikisearch(self, ctx, *, query):
        await ctx.send(wikipedia.search(query))

def setup(client):
    client.add_cog(lookup(client))
    
