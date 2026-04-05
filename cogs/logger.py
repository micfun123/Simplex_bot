import discord
from discord.ext import commands
from discord import option
import aiosqlite
import asyncio
from datetime import datetime

class Logging(commands.Cog):
    """🛠️ Comprehensive server logging to track messages, members, and more."""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/log.db"
        self._cache = {} # guild_id: {channel_id: int, log_bots: bool}

    async def get_config(self, guild_id: int):
        if guild_id in self._cache:
            return self._cache[guild_id]
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT ChannelID, log_bot FROM log WHERE GuildID = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    config = {"channel": row[0], "bots": bool(row[1])}
                else:
                    config = None
        
        if config:
            self._cache[guild_id] = config
        return config

    # --- Slash Command Group ---
    
    logs = discord.SlashCommandGroup("logs", "Manage server activity logging")

    @logs.command(name="setup", description="Configure the channel for server logs")
    @commands.has_permissions(administrator=True)
    @option("channel", discord.TextChannel, description="Where to send log messages")
    async def setup_logs(self, ctx, channel: discord.TextChannel):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO log (GuildID, ChannelID, log_bot) VALUES (?, ?, 1)
                ON CONFLICT(GuildID) DO UPDATE SET ChannelID = EXCLUDED.ChannelID
            """, (ctx.guild.id, channel.id))
            await db.commit()
        
        self._cache.pop(ctx.guild.id, None)
        await ctx.respond(f"✅ Logging channel set to {channel.mention}")

    @logs.command(name="toggle_bots", description="Toggle whether to log messages/actions from bots")
    @commands.has_permissions(administrator=True)
    async def toggle_bots(self, ctx):
        config = await self.get_config(ctx.guild.id)
        if not config:
            return await ctx.respond("❌ Logging is not set up. Use `/logs setup` first.", ephemeral=True)
        
        new_val = 0 if config["bots"] else 1
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE log SET log_bot = ? WHERE GuildID = ?", (new_val, ctx.guild.id))
            await db.commit()
            
        self._cache.pop(ctx.guild.id, None)
        status = "now" if new_val else "no longer"
        await ctx.respond(f"✅ Bot actions **{status}** being logged.")

    # --- Event Listeners ---

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild: return
        config = await self.get_config(message.guild.id)
        if not config: return
        
        channel = message.guild.get_channel(config["channel"])
        if not channel: return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Content", value=message.content or "[No text content]", inline=False)
        if message.attachments:
            embed.add_field(name="Attachments", value=f"{len(message.attachments)} file(s)")
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot or not after.guild or before.content == after.content: return
        config = await self.get_config(after.guild.id)
        if not config: return

        channel = after.guild.get_channel(config["channel"])
        if not channel: return

        embed = discord.Embed(
            title="📝 Message Edited",
            description=f"**Author:** {after.author.mention}\n**Channel:** {after.channel.mention}\n[Jump to message]({after.jump_url})",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Before", value=before.content or "[No text content]", inline=False)
        embed.add_field(name="After", value=after.content or "[No text content]", inline=False)
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        config = await self.get_config(before.guild.id)
        if not config or (before.bot and not config["bots"]): return
        
        channel = before.guild.get_channel(config["channel"])
        if not channel: return

        # Nickname changes
        if before.nick != after.nick:
            embed = discord.Embed(title="👤 Nickname Changed", color=discord.Color.blue(), timestamp=datetime.utcnow())
            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)
            embed.add_field(name="Before", value=before.nick or "None")
            embed.add_field(name="After", value=after.nick or "None")
            await channel.send(embed=embed)

        # Role changes
        if before.roles != after.roles:
            added = [r.mention for r in after.roles if r not in before.roles]
            removed = [r.mention for r in before.roles if r not in after.roles]
            
            if added or removed:
                embed = discord.Embed(title="🛡️ Roles Updated", color=discord.Color.orange(), timestamp=datetime.utcnow())
                embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)
                if added: embed.add_field(name="Added", value=", ".join(added), inline=False)
                if removed: embed.add_field(name="Removed", value=", ".join(removed), inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        config = await self.get_config(guild.id)
        if not config: return
        channel = guild.get_channel(config["channel"])
        if channel:
            embed = discord.Embed(title="🔨 Member Banned", description=f"{user.mention} ({user})", color=discord.Color.dark_red(), timestamp=datetime.utcnow())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        config = await self.get_config(guild.id)
        if not config: return
        channel = guild.get_channel(config["channel"])
        if channel:
            embed = discord.Embed(title="🔓 Member Unbanned", description=f"{user.mention} ({user})", color=discord.Color.green(), timestamp=datetime.utcnow())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        config = await self.get_config(channel.guild.id)
        if not config: return
        log_channel = channel.guild.get_channel(config["channel"])
        if log_channel:
            embed = discord.Embed(title="📁 Channel Created", description=f"**Name:** {channel.name}\n**Category:** {channel.category}", color=discord.Color.green(), timestamp=datetime.utcnow())
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        config = await self.get_config(channel.guild.id)
        if not config: return
        log_channel = channel.guild.get_channel(config["channel"])
        if log_channel:
            embed = discord.Embed(title="🗑️ Channel Deleted", description=f"**Name:** {channel.name}\n**Category:** {channel.category}", color=discord.Color.red(), timestamp=datetime.utcnow())
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(f"❌ You need `{', '.join(error.missing_permissions)}` permissions.", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(f"❌ I'm missing `{', '.join(error.missing_permissions)}` permissions.", ephemeral=True)

def setup(bot):
    bot.add_cog(Logging(bot))
