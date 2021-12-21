import discord
from discord.ext import commands
import json

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

    
def setup(client):
    client.add_cog(Moderation(client))
