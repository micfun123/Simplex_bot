# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json
import random
import os

def mic(ctx):
    return ctx.author.id == 481377376475938826

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="invite", description="Creates 10 day invite for this server")
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.respond(link)

    @commands.slash_command(name="botinvite", description="Invite simplex to your server :)")
    async def botinvite(self, ctx):
        await ctx.respond(embed=discord.Embed(title="Invite **'Simplex'?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @commands.slash_command(name="suggest", description="Suggest something for Simplex bot")
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(908969607266730005)
        await sid.respond(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.respond("Thank you for you suggestion!")

    @commands.slash_command(name="ping", description="shows you the bots ping")
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.client.latency * 1000)}ms")


    
    @slash_command(name="reload", description="reloads a cog")
    @commands.check(mic)
    async def reload(self, ctx, extension:Option(str, "Cog Name", required=True, choices=cogs)):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Slash(client))