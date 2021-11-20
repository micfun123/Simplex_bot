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

            
def setup(client):
    client.add_cog(Moderation(client))
