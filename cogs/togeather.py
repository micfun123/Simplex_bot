import discord
from discord.ext import commands, tasks
from discord_together import DiscordTogether



import os

from requests import options

TOKENfrombot = os.getenv("DISCORD_TOKEN")

class TogetherCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.togetherControl = await DiscordTogether(TOKENfrombot) 
        # Remember to only use this if you haven't already made a bot variable for `togetherControl` in your bot.py file.
        # If you have already declared a bot variable for it, you can use `self.client.togetherControl` to access it's functions

    @commands.command(name="activity", aliases=["together"], help="Join a voice channel with another user to play a game")
    async def activity__dot(self, ctx, *, activity):
        # Here we consider that the user is already in a VC accessible to the bot.
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel")
            return
        else:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id,activity)
            await ctx.send(f"Click the blue link!\n{link}")

    @commands.slash_command(name="activity", description="Join a voice channel with another user to play a game")
    async def activity__slash(self, ctx, *, activity):
        # Here we consider that the user is already in a VC accessible to the bot.
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
            return
        else:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id,activity)
            await ctx.respond(f"Click the blue link!\n{link}")

def setup(client):
    client.add_cog(TogetherCog(client))