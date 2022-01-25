# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json
import random
import os

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
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")

    @commands.slash_command(name="ping", description="shows you the bots ping")
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.client.latency * 1000)}ms")


    #gets user info of user on the discord
    @commands.slash_command(aliases=["userinfo"] ,help = "Finds info about users on the discord.")
    async def info(ctx, user: discord.Member):
         embed = discord.Embed(title=f"{user}'s info", description=f"Here's {user}'s info", color=0x00ff00)
         embed.add_field(name="Username:", value=user.name, inline=True)
         embed.add_field(name="ID:", value=user.id, inline=True)
         embed.add_field(name="Status:", value=user.status, inline=True)
         embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
         embed.add_field(name="Joined:", value=user.joined_at, inline=True)
         embed.set_thumbnail(url=user.avatar_url)
         await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Slash(client))