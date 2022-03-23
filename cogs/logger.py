    
import json
from discord import Option
import discord
from discord.ext import commands
import discord.ui 


async def get_data():
    with open("./databases/log.json") as f:
        data = json.load(f)
    return data


async def dump_data(data):
    with open("./databases/log.json", "w") as f:
        json.dump(data, f, indent=4)

    
class Moderationsettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    #This bit not working \/   \/

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        data = await get_data()
        for i in data:
            if i['guild_id'] == message.author.guild.id:
                stuff = i

        channel = stuff['channel']
       
        channel = await self.client.fetch_channel(channel)
        embed = discord.Embed(
            title="{}'s message deleted.".format(message.author.name), #message.author is sender of the message
            description=message.content,
            color=discord.Color.red()
        )
        await channel.send(embed=embed) 


#This bit not working^^

    @commands.command()
    async def setLogChannel(self, ctx, channel: discord.TextChannel):
        data = await get_data()
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['channel'] = channel.id
        await dump_data(data)
        await ctx.send(f"Set log channel to {channel.mention}")

    @commands.command()
    @commands.is_owner()
    async def set_all_log(self, ctx):
        data = await get_data()
        for guild in self.client.guilds:
            append_this = {
                "guild_id": guild.id,
                "channel": None,
        
            }
            data.append(append_this)

        await dump_data(data)
        await ctx.send("Done")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = await get_data()

        append_this = {
            "guild_id": guild.id,
            "channel": None,
            
        }
        data.append(append_this)

        await dump_data(data)

def setup(client):
    client.add_cog(Moderationsettings(client))

