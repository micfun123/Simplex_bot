import imp
import discord
from discord.ext import commands
import json
import os

def mic(ctx):
    return ctx.author.id == 481377376475938826

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
    async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)
            
     

    @commands.has_permissions(kick_members=True)  #warn a user with Dms
    @commands.command(help = "Dms the User with a warning")
    async def warn(ctx, user: discord.User, *, message=None):
        message = message or "This Message is a warning"
        await discord.User.send(user, message + (f"** Warned by {ctx.message.author} From server {message.server.name}**"))

    @commands.command(name="removereactions",help="Clear reactions from a message in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def removereactions(self, ctx, id:int):
        message = await ctx.channel.fetch_message(id)
        await message.clear_reactions()
        await ctx.send("Removed")
        
    @commands.command()
    @commands.check(mic)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)
  
    @commands.command()
    @commands.check(mic)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        await ctx.send(f"Connected on {str(len(servers))} servers:")
        await ctx.send('\n'.join(guild.name for guild in servers))

    @commands.command(aliases=['sendmsg'])
    @commands.check(mic)
    async def dm(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)

def setup(client):
    client.add_cog(Moderation(client))
