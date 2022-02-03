import imp
from pydoc import describe
from discord import Embed
import wikipedia
from discord.ext import commands
import json
import os
from tools import log
import discord


class lookup(commands.Cog):
    def __init__(self, client): 
        self.client = client 


    @commands.command()
    async def wiki(self, ctx, *, query):
        await ctx.send(wikipedia.summary(query, sentences=20))
        log(query + " was looked up on wikipedia")


def setup(client):
    client.add_cog(lookup(client))
    
