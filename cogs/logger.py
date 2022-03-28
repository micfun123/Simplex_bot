    
import json
from discord import Option
import discord
from discord.ext import commands
import discord.ui 


async def get_data_announcement():
    with open("./databases/announcement.json") as f:
        data = json.load(f)
    return data


async def dump_data_announcement(data):
    with open("./databases/announcement.json", "w") as f:
        json.dump(data, f, indent=4)

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

    @commands.command()
    async def announcement(self, ctx, *, message):
        data = await get_data_announcement()
        for guild in data:
            stuff = guild
        channel = await self.client.fetch_channel(channel)
        channel = stuff['channel']
    
        await channel.send(message) 


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



    @commands.command()
    async def setLogChannel(self, ctx, channel: discord.TextChannel):
        data = await get_data()
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['channel'] = channel.id
        await dump_data(data)
        await ctx.send(f"Set log channel to {channel.mention}")

    @commands.command()
    async def setAnnouncementChannel(self, ctx, channel: discord.TextChannel):
        data = await get_data_announcement()
        for i in data:
            if i['guild_id'] == ctx.guild.id:
                i['channel'] = channel.id
        await dump_data_announcement(data)
        await ctx.send(f"Set log channel to {channel.mention}")

    @commands.command(hidden = True)
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

    @commands.command(hidden = True)
    @commands.is_owner()
    async def set_all_announcement(self, ctx):
        data = await get_data_announcement()
        for guild in self.client.guilds:
            append_this = {
                "guild_id": guild.id,
                "channel": None,
        
            }
            data.append(append_this)

        await dump_data_announcement(data)
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

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = await get_data_announcement()

        append_this = {
            "guild_id": guild.id,
            "channel": None,
            
        }
        data.append(append_this)

        await dump_data_announcement(data)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.client.user.id:
            return
        em = discord.Embed(color=discord.Color.blue(), 
            title="Message Edit", description=f"{before.author} edited their message")
        em.add_field(name="Before", value=before.content)
        em.add_field(name="After", value=after.content)

        data = await get_data()
        for i in data:
            if i['guild_id'] == after.author.guild.id:
                stuff = i

                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
            
            await channel.send(embed=em)

def setup(client):
    client.add_cog(Moderationsettings(client))

