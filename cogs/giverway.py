import discord
import datetime
import random
from discord.ext import commands
import os
import json

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client


        
def setup(client):
    client.add_cog(Giveaway(client)) 