import os
import asyncio
import aiosqlite
import feedparser
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.ext import tasks
import httpx

class RSSManager(commands.Cog):
    """📬 Manage your RSS feeds here."""

    def __init__(self, bot):
        self.bot = bot
        self.rss_loop.start()

    def cog_unload(self):
        self.rss_loop.cancel()

    rss = SlashCommandGroup("rss", "RSS related commands")

    @rss.command(name="add", description="Add RSS feeds to your server")
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, name, channel, feed):
        feed_URL = feed
        async with aiosqlite.connect("databases/rss.db") as db:
            cursor = await db.execute("SELECT * FROM rss WHERE guild = ?", (str(ctx.guild.id),))
            feeds = await cursor.fetchall()


        channel_id_str = channel.replace("<#", "").replace(">", "")
        try:
            channel_id = int(channel_id_str)
            target_channel = self.bot.get_channel(channel_id)
            if target_channel is None:
                target_channel = await self.bot.fetch_channel(channel_id)
        except Exception:
            await ctx.respond("That channel does not exist or is not accessible.")
            return

        # Validate RSS feed
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(feed_URL, timeout=10.0)
                feed_data = feedparser.parse(resp.text)
                if not feed_data.entries:
                    raise ValueError
        except Exception:
            await ctx.respond("That is not a valid RSS feed.")
            return

        # Save to DB
        async with aiosqlite.connect("databases/rss.db") as db:
            await db.execute(
                "INSERT INTO rss (name, url, channel, guild, lastpost) VALUES (?, ?, ?, ?, ?)",
                (name, feed_URL, str(channel_id), str(ctx.guild.id), None)
            )
            await db.commit()

        await ctx.respond("Done adding feed. Sending a test message...")
        try:
            await target_channel.send(
                "✅ RSS feed added successfully! New entries will be posted here. \n If you like this feature, consider donating to support the bot: https://buymeacoffee.com/michaelrbparker"
            )
        except:
            pass

    @rss.command(name="list", description="Lists all RSS feeds in this server")
    @commands.has_permissions(manage_guild=True)
    async def list_feeds(self, ctx):
        async with aiosqlite.connect("databases/rss.db") as db:
            cursor = await db.execute("SELECT * FROM rss WHERE guild = ?", (str(ctx.guild.id),))
            rows = await cursor.fetchall()

        if not rows:
            await ctx.respond("No feeds have been added yet.")
        else:
            embed = discord.Embed(title="📬 RSS Feeds", color=0x00FF00)
            for name, url, *_ in rows:
                embed.add_field(name=name, value=url, inline=False)
            await ctx.respond(embed=embed)

    @rss.command(name="remove", description="Removes an RSS feed from this server")
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, feedname: str):
        async with aiosqlite.connect("databases/rss.db") as db:
            await db.execute(
                "DELETE FROM rss WHERE name = ? AND guild = ?",
                (feedname, str(ctx.guild.id))
            )
            await db.commit()
        await ctx.respond(f"Feed '{feedname}' has been removed.")

    @commands.command(name="removeinvalid", help="Removes any invalid RSS feeds from this server")
    @commands.has_permissions(manage_guild=True)
    async def remove_invalid(self, ctx):
        await ctx.defer()
        invalid_feeds = []
        async with aiosqlite.connect("databases/rss.db") as db:
            cursor = await db.execute("SELECT name, url FROM rss WHERE guild = ?", (str(ctx.guild.id),))
            rows = await cursor.fetchall()
            
            if not rows:
                await ctx.respond("No feeds have been added yet.")
                return
            
            async with httpx.AsyncClient() as client:
                for name, url in rows:
                    is_invalid = False
                    try:
                        resp = await client.get(url, timeout=10.0)
                        feed_data = feedparser.parse(resp.text)
                        if not feed_data.entries:
                            is_invalid = True
                    except Exception:
                        is_invalid = True
                        
                    if is_invalid:
                        invalid_feeds.append(name)
                        await db.execute("DELETE FROM rss WHERE name = ? AND guild = ?", (name, str(ctx.guild.id)))
            
            if invalid_feeds:
                await db.commit()
                removed_list = ", ".join(invalid_feeds)
                await ctx.respond(f"Removed invalid feeds: {removed_list}")
            else:
                await ctx.respond("No invalid feeds found.")

    @tasks.loop(minutes=30)
    async def rss_loop(self):
        try:
            async with aiosqlite.connect("databases/rss.db") as db:
                async with db.execute("SELECT name, url, channel, guild, lastpost FROM rss") as cursor:
                    rows = await cursor.fetchall()
                
                async with httpx.AsyncClient() as client:
                    for row in rows:
                        name, url, channel_id, guild_id, lastpost = row
                        try:
                            resp = await client.get(url, timeout=15.0)
                            feed = feedparser.parse(resp.text)
                            if not feed.entries:
                                continue

                            latest_entry = feed.entries[0]
                            checkpost = latest_entry.get("link")

                            if not checkpost or checkpost == lastpost:
                                continue

                            title = latest_entry.get("title", "No title")
                            message = f"**{title}**\n{checkpost}"

                            target_channel = self.bot.get_channel(int(channel_id))
                            if not target_channel:
                                target_channel = await self.bot.fetch_channel(int(channel_id))
                            
                            await target_channel.send(message)
                            await db.execute("UPDATE rss SET lastpost = ? WHERE url = ? AND guild = ?", (checkpost, url, guild_id))
                            await db.commit()
                        except Exception as e:
                            print(f"RSS Loop error for {url}: {e}")
                            # remove invalid feed from database 
                            await db.execute("DELETE FROM rss WHERE url = ? AND guild = ?", (url, guild_id))
                            await db.commit()
                            
                        
                        await asyncio.sleep(1) # Small delay between feeds
        except Exception as e:
            print(f"Main RSS Loop error: {e}")

    @rss_loop.before_loop
    async def before_rss_loop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RSSManager(bot))
