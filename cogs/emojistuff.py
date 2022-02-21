import datetime
import discord
from discord.ext import commands
from tools import log

class emoji(commands.Cog):
    """All emoji stuff"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(emoji(bot))