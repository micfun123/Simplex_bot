import imp
from pydoc import describe
from this import s
from discord import Embed
import wikipedia
from discord.ext import commands
import json
import os
import discord
import imp
import traceback
from tools import log

def printError(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    print(traceback_text)
    log(traceback_text)
class lookup(commands.Cog):
    def __init__(self, client): 
        self.client = client 




    @commands.command()
    async def wiki(self, ctx, *, query):
        embed = Embed(title="Wikipedia", description="Searching for {}".format(query), color=0x00ff00)
        page = wikipedia.summary(query, chars=1000)
        url = wikipedia.page(query).url
        embed.add_field(name="Description", value=page)
        embed.add_field(name="Link", value=url ,inline=False)
        await ctx.send(embed=embed)
       

def setup(client):
    client.add_cog(lookup(client))
    
