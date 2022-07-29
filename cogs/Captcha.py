import discord
from discord.ext import commands
import asyncio

class Captcha(commands.Cog):
    def __init__(self, client):
        self.client = client
    

def setup(client):
    client.add_cog(Captcha(client))