    
from tools import mic, log
import json
from discord import Option
import discord
from discord.ext import commands
import discord.ui 
import datetime


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
    @commands.is_owner()
    async def announcement(self, ctx, *, message):
        data = await get_data_announcement()
        for guild in data:
            stuff = guild
            y = stuff['channel']
            if y == None:
                continue
            channel = await self.client.fetch_channel(y)
            try:
                await channel.send(message)
            except:
                log(f"{channel} does not have perms for announcement")

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
        await ctx.send(f"Set bot announcment channel to {channel.mention}")

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
        em.add_field(name="Channel", value=after.channel)
        em.add_field(name="Link", value=f"https://discordapp.com/channels/{after.guild.id}/{after.channel.id}/{after.id}")
        em.set_footer(text=f"{after.created_at}")
        

        data = await get_data()
        for i in data:
            if i['guild_id'] == after.author.guild.id:
                stuff = i

                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick is not None and after.nick is None:
            em = discord.Embed(color=discord.Color.blue(), title="Nick Change",
                                description=f"{before.name} has unicked", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value=before.nick)
            em.add_field(name="After:", value="No Nick")

        if before.nick is None and after.nick is not None:
            em = discord.Embed(color=discord.Color.blue(), title="Nick Change",
                                description=f"{before.name} Has nicked", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value="No Nick")
            em.add_field(name="After:", value=after.nick)

        elif before.nick != after.nick:
            em = discord.Embed(color=discord.Color.blue(), 
                title="Nick Change", description=f"{before.name} Has changed their nick", timestamp = datetime.datetime.utcnow())
            em.add_field(name="Before:", value=before.nick)
            em.add_field(name="After:", value=after.nick)

        data = await get_data()
        for i in data:
            if i['guild_id'] == before.guild.id:
                stuff = i
                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        em = discord.Embed(color=discord.Color.blue(), 
            title="Member Banned!", description=f"{user.name} Has been banned from the server", timestamp = datetime.datetime.utcnow())
        data = await get_data()
        for i in data:
            if i['guild_id'] == user.guild.id:
                stuff = i
                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        em = discord.Embed(color=discord.Color.blue(), 
            title="Member Unbanned!", description=f"{user.name} Has been unbanned from the server", timestamp = datetime.datetime.utcnow())
        data = await get_data()
        for i in data:
            if i['guild_id'] == user.guild.id:
                stuff = i
                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        em = discord.Embed(color=discord.Color.blue(), 
            title="Channel deleted!", description=f"{channel.name} Has been deleated from the server", timestamp = datetime.datetime.utcnow())
        em.add_field(name="Channel:", value=channel.name)
        data = await get_data()
        for i in data:
            if i['guild_id'] == channel.guild.id:
                stuff = i
                y = stuff['channel']
                channel = await self.client.fetch_channel(y)
                await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        em = discord.Embed(color=discord.Color.blue(),
            title="Channel Created!", description=f"{channel.name} Has been created on the server", timestamp = datetime.datetime.utcnow())
        data = await get_data()
        for i in data:
           if i['guild_id'] == channel.guild.id:
               stuff = i
               y = stuff['channel']
               channel = await self.client.fetch_channel(y)
               await channel.send(embed=em)




def setup(client):
    client.add_cog(Moderationsettings(client))

