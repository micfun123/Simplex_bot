import discord
from discord.ext import commands, tasks
from discord import option
import aiosqlite
import httpx
import os
import asyncio
import logging
import re
from mastodon import Mastodon
from datetime import datetime

# Setup logging
logger = logging.getLogger("simplex.mastodon")

class MastodonFeed(commands.Cog):
    """🐘 Follow Mastodon accounts and post updates to Discord!"""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/mastodon.db"
        self._clients = {} # Cache for instance clients
        self.mastodon_loop.start()

    def get_client(self, instance="mastodon.social"):
        """Get or create a Mastodon client for a specific instance."""
        if instance in self._clients:
            return self._clients[instance]
        
        # Note: If you need instance-specific tokens, you'd load them here.
        # Defaulting to the global tokens for mastodon.social for now.
        client = Mastodon(
            client_id=os.getenv("MASTODON_CLIENT_ID"),
            client_secret=os.getenv("MASTODON_CLIENT_SECRET"),
            access_token=os.getenv("MASTODON_ACCESS_TOKEN"),
            api_base_url=f"https://{instance}"
        )
        self._clients[instance] = client
        return client

    def cog_unload(self):
        self.mastodon_loop.cancel()

    # Slash Command Group
    mastodon = discord.SlashCommandGroup("mastodon", "Mastodon feed commands")

    @mastodon.command(name="add", description="Add a Mastodon account to follow")
    @commands.has_permissions(manage_channels=True)
    @option("channel", discord.TextChannel, description="The channel to post updates in")
    @option("account", str, description="The account (e.g., username or user@instance.com)")
    async def add_mastodon(self, ctx, channel: discord.TextChannel, account: str):
        """Start following a Mastodon account."""
        await ctx.defer()
        
        # Parse user and instance
        if "@" in account:
            username, instance = account.split("@", 1)
        else:
            username, instance = account, "mastodon.social"

        try:
            # Verify user exists and get their ID
            client = self.get_client(instance)
            results = client.account_search(username)
            if not results:
                return await ctx.respond(f"❌ Could not find user **{username}** on **{instance}**.", ephemeral=True)
            
            target_user = results[0]
            user_id = target_user["id"]
            
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO mastodon (channel_id, guild_id, username, instance, mastodon_user_id, last_posted)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (channel.id, ctx.guild.id, username, instance, str(user_id), "0"))
                await db.commit()
                
            await ctx.respond(f"✅ Now following **{username}@{instance}** in {channel.mention}!")
        except Exception as e:
            logger.error(f"Failed to add Mastodon account: {e}")
            await ctx.respond("❌ An error occurred while adding the account. Check if the instance is correct.", ephemeral=True)

    @mastodon.command(name="remove", description="Remove a Mastodon account from following")
    @commands.has_permissions(manage_channels=True)
    @option("channel", discord.TextChannel, description="The channel the feed was in")
    @option("account", str, description="The account to remove (username or user@instance)")
    async def remove_mastodon(self, ctx, channel: discord.TextChannel, account: str):
        """Stop following a Mastodon account."""
        if "@" in account:
            username, instance = account.split("@", 1)
        else:
            username, instance = account, "mastodon.social"

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                DELETE FROM mastodon 
                WHERE channel_id = ? AND username = ? AND instance = ?
            """, (channel.id, username, instance))
            await db.commit()
            
        await ctx.respond(f"✅ Stopped following **{username}@{instance}** in {channel.mention}.")

    @mastodon.command(name="list", description="List followed Mastodon accounts in this server")
    async def list_mastodon(self, ctx):
        """Show all Mastodon feeds for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT channel_id, username, instance FROM mastodon WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
                
        if not rows:
            return await ctx.respond("❌ No Mastodon feeds are set up on this server.")
            
        embed = discord.Embed(title=f"🐘 Mastodon Feeds for {ctx.guild.name}", color=0x2b90d9)
        for channel_id, username, instance in rows:
            channel = ctx.guild.get_channel(channel_id)
            embed.add_field(
                name=f"{username}@{instance}",
                value=f"Channel: {channel.mention if channel else 'Deleted Channel'}",
                inline=False
            )
        await ctx.respond(embed=embed)

    @tasks.loop(minutes=10)
    async def mastodon_loop(self):
        """Check for new posts from followed Mastodon accounts."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT channel_id, username, instance, mastodon_user_id, last_posted FROM mastodon") as cursor:
                rows = await cursor.fetchall()

        for channel_id, username, instance, user_id, last_posted in rows:
            try:
                client = self.get_client(instance)
                
                # Fetch newest status
                statuses = client.account_statuses(user_id, limit=1)
                if not statuses:
                    continue
                
                latest = statuses[0]
                status_id = str(latest["id"])
                
                if status_id != last_posted:
                    channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
                    if not channel:
                        continue

                    # Process content to strip HTML tags
                    content = re.sub('<[^<]+?>', '', latest["content"])
                    url = latest["url"]
                    
                    message = f"**{username}** just posted on Mastodon:\n{url}\n\n{content}"
                    if len(message) > 2000:
                        message = message[:1997] + "..."

                    await channel.send(message)
                    
                    # Update DB
                    async with aiosqlite.connect(self.db_path) as db:
                        await db.execute("UPDATE mastodon SET last_posted = ? WHERE channel_id = ? AND username = ? AND instance = ?", (status_id, channel_id, username, instance))
                        await db.commit()
                
                # Sleep briefly between requests to avoid rate limits
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error checking Mastodon feed {username}@{instance}: {e}")

    @mastodon_loop.before_loop
    async def before_mastodon_looper(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(MastodonFeed(bot))
