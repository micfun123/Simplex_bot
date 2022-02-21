import imp
import discord
from discord.ext import commands
import json
import os
from os import listdir
from os.path import isfile, join
import datetime

def micsid(ctx):
    return ctx.author.id == 481377376475938826 or ctx.author.id == 624076054969188363


def log(log):
    now = datetime.now()
    timern = now.strftime("%d/%m/%Y %H:%M:%S")

    with open('./other/log.txt', 'a') as f:
        f.write('\n')
        f.write(f"{timern} | {log}")

  

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])

class Moderation(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        embedVar = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=embedVar)
        await msg.add_reaction(emoji)
        with open("react.json") as json_file:
            data = json.load(json_file)

            new_react_role = {
                "role_name": role.name,
                "role_id": role.id,
                "emoji": emoji,
                "message_id": msg.id,
            }

            data.append(new_react_role)

        with open("react.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.has_permissions(kick_members=True)  #kicks a person
    @commands.command(help = "kicks a person from server")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)
            
     

    @commands.has_permissions(kick_members=True)  #warn a user with Dms
    @commands.command(help = "Dms the User with a warning")
    async def warn(self, ctx, user: discord.User, *, message=None):
        message = message or "This Message is a warning"
        await discord.User.send(user, message + (f"** Warned by {ctx.message.author} From server {message.server.name}**"))

    @commands.command(name="removereactions",help="Clear reactions from a message in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")
        
    @commands.command()
    @commands.check(micsid)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)
  
    @commands.command()
    @commands.check(micsid)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        guild = self.client.get_guild(id)
        serprint = '\n'.join(guild.name +' | '+str(guild.member_count) +' | ' + str(guild.owner.name) + ' | ' + str(guild.owner.id) for guild in servers)
        embed = discord.Embed(title=f"Connected on {str(len(servers))} servers:" , description=f"{serprint}", color=0xff00c8)
       
        await ctx.send(embed=embed)

    @commands.command(aliases=['sendmsg'])
    @commands.check(micsid)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        role = ctx.guild.default_role

        if role not in channel.overwrites:
            overwrites = {
                role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown", color=discord.Colour.orange()))
        elif channel.overwrites[role].send_messages is True or \
                channel.overwrites[role].send_messages is None:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown.", color=discord.Colour.orange()))
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is no longer under lockdown.", color=discord.Colour.orange()))



def setup(client):
    client.add_cog(Moderation(client))
