import discord
import json
from discord.ext import commands
from datetime import datetime

class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Sets the autorole for the server")
    async def autorole(self, ctx, role:discord.Role):
        role_id = role.id
        guild_id = str(ctx.guild.id)

        with open("./databases/autorole.json") as f:
            data = json.load(f)

        data[guild_id] = role_id
        
        with open("./databases/autorole.json", 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(embed=discord.Embed(title=f"{role.mention} has been set as the autorole for this server"))

    @commands.command()
    async def autorolereset(self, ctx):
        guild_id = str(ctx.guild.id)

        with open("./databases/autorole.json") as f:
            data = json.load(f)

        data[guild_id] = None
        
        with open("./databases/autorole.json", 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(embed=discord.Embed(title="Autorole reset"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./databases/autorole.json") as f:
            data = json.load(f)
        
        if str(member.guild.id) not in data or str(member.guild.id) is None:
            return
        
        role = data[str(member.guild.id)]

        role = member.guild.get_role(role)
        await member.add_roles(role)

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),f"| Member: {member.name} Was given role: {role.name}")

def setup(client):
    client.add_cog(Autorole(client))