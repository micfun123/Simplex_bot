import discord
from discord.ext import commands, tasks
from discord import option
import aiosqlite
import httpx
import os
import asyncio
import logging
from datetime import datetime, time



class Events(commands.Cog):
    """Bot event listeners and handlers."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("------------------------------------")
        print(f"✅ Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------------------------------------")
        await self.update_status()


    async def update_status(self):
            await self.bot.change_presence(
                activity=discord.Game(name=f"been a good boy on {len(self.bot.guilds)} servers!")
            )

    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.update_status()


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.update_status()

    @commands.command(name="status", help="Check the bot's current status")
    async def status(self, ctx):
        """Check the bot's current status."""
        await ctx.send(f"✅ I'm currently active in {len(self.bot.guilds)} servers!")
        await self.update_status()

def setup(bot):
    bot.add_cog(Events(bot))
