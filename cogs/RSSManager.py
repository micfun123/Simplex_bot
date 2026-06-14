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
            loop = asyncio.get_event_loop()
            async with httpx.AsyncClient() as client:
                resp = await client.get(feed_URL, timeout=10.0)
                feed_data = await loop.run_in_executor(None, feedparser.parse, resp.text)
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
            
            loop = asyncio.get_event_loop()
            async with httpx.AsyncClient() as client:
                for name, url in rows:
                    is_invalid = False
                    try:
                        resp = await client.get(url, timeout=10.0)
                        feed_data = await loop.run_in_executor(None, feedparser.parse, resp.text)
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

    async def _check_feeds(self, guild_id_filter=None):
        """Check every stored feed (optionally scoped to one guild) and post new entries.

        Returns the number of new posts sent.
        """
        posted = 0
        try:
            async with aiosqlite.connect("databases/rss.db") as db:
                if guild_id_filter is None:
                    query = "SELECT name, url, channel, guild, lastpost FROM rss"
                    params = ()
                else:
                    query = "SELECT name, url, channel, guild, lastpost FROM rss WHERE guild = ?"
                    params = (str(guild_id_filter),)
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()

            loop = asyncio.get_event_loop()
            async with httpx.AsyncClient() as client:
                for name, url, channel_id, guild_id, lastpost in rows:
                    try:
                        resp = await client.get(url, timeout=15.0)
                        if resp.status_code in (301, 302, 404, 402, 410):
                            async with aiosqlite.connect("databases/rss.db") as db:
                                await db.execute("DELETE FROM rss WHERE url = ? AND guild = ?", (url, guild_id))
                                await db.commit()
                            print(f"RSS: removed dead feed {url} (HTTP {resp.status_code})")
                            continue
                        feed = await loop.run_in_executor(None, feedparser.parse, resp.text)
                        if not feed.entries:
                            continue

                        latest_entry = feed.entries[0]
                        checkpost = latest_entry.get("link")
                        if not checkpost or checkpost == lastpost:
                            continue

                        title = latest_entry.get("title", "No title")
                        msg = f"**{title}**\n{checkpost}"

                        target_channel = self.bot.get_channel(int(channel_id))
                        if not target_channel:
                            target_channel = await self.bot.fetch_channel(int(channel_id))

                        await target_channel.send(msg)
                        posted += 1
                        async with aiosqlite.connect("databases/rss.db") as db:
                            await db.execute("UPDATE rss SET lastpost = ? WHERE url = ? AND guild = ?", (checkpost, url, guild_id))
                            await db.commit()
                    except Exception as e:
                        print(f"RSS Loop error for {url}: {e}")
                    await asyncio.sleep(0)
        except Exception as e:
            print(f"Main RSS Loop error: {e}")
        return posted

    @tasks.loop(hours=1)
    async def rss_loop(self):
        await self._check_feeds()

    @rss.command(name="force", description="Force-check this server's RSS feeds right now")
    @commands.has_permissions(manage_guild=True)
    async def force(self, ctx):
        """Immediately check this server's RSS feeds for new posts."""
        await ctx.defer()
        posted = await self._check_feeds(guild_id_filter=ctx.guild.id)
        await ctx.respond(f"✅ RSS check complete — posted {posted} new {'entry' if posted == 1 else 'entries'}.")

    @rss_loop.before_loop
    async def before_rss_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(300)

def setup(bot):
    bot.add_cog(RSSManager(bot))
