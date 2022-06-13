import imp
from discord.ext import commands
import asyncio
import os
import json


class Birthday(commands.Cog):
    """Birthday commands."""

    def __init__(self, bot):
        self.bot = bot

    


def setup(bot):
    bot.add_cog(Birthday(bot))


