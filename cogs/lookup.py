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




    @commands.command()
    async def wiki(self, ctx, *, query):
        embed = Embed(title="Wikipedia", description="Searching for {}".format(query), color=0x00ff00)
        page = wikipedia.summary(query, sentences=250)
        url = wikipedia.page(query).url
        embed.description = page
        embed.add_field(name="Link", value=url ,inline=False)
        await ctx.send(embed=embed)
       

def setup(client):
    client.add_cog(lookup(client))
    
