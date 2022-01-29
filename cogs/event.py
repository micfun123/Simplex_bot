import discord
from discord.ext import commands
import json
from datetime import datetime



async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))
    print("Updated presence")

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cha = self.client.get_channel(925787897527926805)
        await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))
        await update_activity(self.client)
       
            

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925787897527926805)
        await cha.send(embed=discord.Embed(title="Leave", description=f"Left: {guild.name}"))

def setup(client):
    client.add_cog(Events(client))