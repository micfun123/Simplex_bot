import os
import asyncio
import aiosqlite
import feedparser
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import httpx as requests  # httpx is async-capable, but you're using it sync here
import aiohttp

class RSSManager(commands.Cog):
    """📬 Manage your RSS feeds here."""

    def __init__(self, bot):
        self.bot = bot

    rss = SlashCommandGroup("rss", "RSS related commands")

    @rss.command(name="add", description="Add RSS feeds to your server")
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, name, channel, feed):
        print(name,channel,feed)
        feed_URL = feed
        async with aiosqlite.connect("databases/rss.db") as db:
            cursor = await db.execute("SELECT * FROM rss WHERE guild = ?", (str(ctx.guild.id),))
            feeds = await cursor.fetchall()

        if len(feeds) >= 2:
            token = os.getenv("TOPGG_TOKEN")
            try:
                response = requests.get(
                    f"https://top.gg/api/bots/902240397273743361/check?userId={ctx.author.id}",
                    headers={"Authorization": token}
                )
                data = response.json()
                voted = data.get("voted", 0)
            except Exception as e:
                print(f"TopGG API error: {e}")
                voted = 1
            if response.status_code != 200 or voted == 0:
                await ctx.respond(
                    "You can have more than 2 RSS feeds only if you've voted in the last 24h. Vote here: https://top.gg/bot/902240397273743361/vote",
                    ephemeral=True
                )
                return

       
        channel_id_str = channel.replace("<#", "").replace(">", "")
        try:
            channel_id = int(channel_id_str)
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                raise ValueError
        except Exception:
            await ctx.respond("That channel does not exist or is not accessible.")
            return

        # Validate RSS feed
        try:
            feed = feedparser.parse(feed)
            if not feed.entries:
                raise ValueError
        except Exception:
            await ctx.respond("That is not a valid RSS feed.")
            return

        # Save to DB
        async with aiosqlite.connect("databases/rss.db") as db:
            await db.execute(
                "INSERT INTO rss VALUES (?, ?, ?, ?, ?)",
                (name, feed_URL, str(channel_id), str(ctx.guild.id), None)
            )
            await db.commit()

        await ctx.respond("Done adding feed. Sending a test message to the selected channel...")
        try:
            await channel.send(
                "This is a test message. We'll check this feed every 12 hours and post new entries here."
            )
            await ctx.respond("Test message sent! Make sure the bot has permission to send messages in that channel.")
        except Exception as e:
            await ctx.respond(f"Failed to send test message: {e}")

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
        try:
            async with aiosqlite.connect("databases/rss.db") as db:
                await db.execute(
                    "DELETE FROM rss WHERE name = ? AND guild = ?",
                    (feedname, str(ctx.guild.id))
                )
                await db.commit()
                await db.close()

            await ctx.respond(f"Feed '{feedname}' has been removed.")
        except:
            await ctx.respond(f"Unable to find feed. please check spelling and spacing of your rss feeds name")

    @commands.command()
    @commands.is_owner()
    async def remove_invalid_rss(self, ctx):
        removed = 0
        await ctx.send("🔍 Removing invalid RSS feeds...")

        async with aiosqlite.connect("databases/rss.db") as db:
            # Step 1: Remove feeds with NULL lastpost that are invalid
            async with db.execute("SELECT * FROM rss WHERE lastpost IS NULL") as cursor:
                rows = await cursor.fetchall()
                print(f"Found {len(rows)} invalid feeds")

                for row in rows:
                    name, url, channel_id, server_id = row[0], row[1], row[2], row[3]
                    try:
                        feed = feedparser.parse(url)
                        if feed.bozo:
                            try:
                                # Notify channel about invalid feed
                                channel = await self.bot.fetch_channel(channel_id)
                                await channel.send(
                                    f"⚠️ RSS feed `{url}` is invalid and has been removed.\n"
                                    "If you believe this is an error, please DM the bot or join the support server."
                                )
                            except Exception as send_error:
                                print(f"Failed to notify channel {channel_id}: {send_error}")

                            # Remove the invalid feed from DB
                            await db.execute(
                                "DELETE FROM rss WHERE name = ? AND guild = ?",
                                (name, server_id)
                            )
                            await db.commit()
                            removed += 1
                    except Exception as e:
                        print(f"Error processing feed '{url}' in guild {server_id}: {e}")
                    await asyncio.sleep(0.5)

            await ctx.send("✅ Removed invalid feeds. Now checking for feeds from servers I'm no longer in...")

            # Step 2: Remove feeds from servers the bot has been removed from
            async with db.execute("SELECT * FROM rss") as cursor:
                rows = await cursor.fetchall()

                for row in rows:
                    name, _, _, server_id = row[0], row[1], row[2], row[3]
                    try:
                        guild = self.bot.get_guild(int(server_id))
                        if guild is None:
                            await db.execute(
                                "DELETE FROM rss WHERE name = ? AND guild = ?",
                                (name, server_id)
                            )
                            await db.commit()
                            removed += 1
                    except Exception as e:
                        print(f"Error checking guild {server_id}: {e}")
                    await asyncio.sleep(0.5)

        await ctx.send(f"✅ Cleanup complete. {removed} feeds removed.")
        await ctx.send("✅ Finished removing invalid RSS feeds.")

def setup(bot):
    bot.add_cog(RSSManager(bot))
