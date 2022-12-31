import aiosqlite
from discord import Guild, Option
import discord
from discord.ext import commands
import discord.ui 
import calendar, datetime, time


async def get_announcement_channel(guild_id):
    async with aiosqlite.connect("databases/announcement.db") as db:
        data = await db.execute("SELECT * FROM server WHERE ServerID = ?", (guild_id,))
        data = await data.fetchall()
        if len(data) == 0:
            return None
        else:
            return data[0][1]

            