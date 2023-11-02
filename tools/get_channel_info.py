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


async def set_announcement_channel_tool(guild_id, channel_id):
    async with aiosqlite.connect("databases/announcement.db") as db:
        data = await db.execute("SELECT * FROM server WHERE ServerID = ?", (guild_id,))
        data = await data.fetchall()
        if len(data) == 0:
            await db.execute("INSERT INTO server VALUES (?, ?)", (guild_id, channel_id))
            await db.commit()
        else:
            await db.execute(
                "UPDATE server SET Channel = ? WHERE ServerID = ?",
                (channel_id, guild_id),
            )
            await db.commit()


async def get_counting_channel(guild_id):
    async with aiosqlite.connect("databases/counting.db") as db:
        data = await db.execute(
            "SELECT * FROM counting WHERE guild_id = ?", (guild_id,)
        )
        data = await data.fetchall()
        if len(data) == 0:
            return None
        else:
            return data[0][1]
