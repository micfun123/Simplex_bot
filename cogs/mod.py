import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import option
import asyncio
import string
import unicodedata
import re

class Moderation(commands.Cog):
    """🛠️ Essential Moderation and Role management tools."""
    
    def __init__(self, bot):
        self.bot = bot

    # Slash Command Groups
    mod = SlashCommandGroup("mod", "General moderation commands")
    role_grp = SlashCommandGroup("role", "Role management commands")

    # --- Mod Group ---

    @mod.command(name="clear_reactions", description="Clear all reactions from a message")
    @commands.has_permissions(manage_messages=True)
    @option("message_id", str, description="The ID of the message to clear reactions from")
    async def clear_reactions(self, ctx: discord.ApplicationContext, message_id: str):
        try:
            msg = await ctx.channel.fetch_message(int(message_id))
            await msg.clear_reactions()
            await ctx.respond("✅ Reactions removed.", ephemeral=True)
        except:
            await ctx.respond("❌ Message not found in this channel.", ephemeral=True)

    @mod.command(name="regex_clear", description="Deletes messages matching a regex pattern")
    @commands.has_permissions(manage_messages=True)
    @option("regex", str, description="The regex pattern to match")
    @option("limit", int, description="How many messages to check", default=100, min_value=1, max_value=500)
    async def regex_clear(self, ctx: discord.ApplicationContext, regex: str, limit: int):
        await ctx.defer(ephemeral=True)
        try:
            pattern = re.compile(regex)
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: pattern.search(m.content))
            await ctx.followup.send(f"🗑️ Deleted {len(deleted)} messages.")
        except Exception as e:
            await ctx.followup.send(f"❌ Error: {e}")

    @mod.command(name="lockdown", description="Locks or unlocks the current channel")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx: discord.ApplicationContext):
        role = ctx.guild.default_role
        current_overwrite = ctx.channel.overwrites_for(role)
        
        if current_overwrite.send_messages is False:
            current_overwrite.send_messages = None
            await ctx.channel.set_permissions(role, overwrite=current_overwrite)
            embed = discord.Embed(title="🔓 Channel unlocked.", color=discord.Color.green())
        else:
            current_overwrite.send_messages = False
            await ctx.channel.set_permissions(role, overwrite=current_overwrite)
            embed = discord.Embed(title="🔒 Channel locked down.", color=discord.Color.orange())
        
        await ctx.respond(embed=embed)


    @mod.command(name="purge_user", description="Deletes all messages from a user in this channel")
    @commands.has_permissions(manage_messages=True)
    @option("member", discord.Member, description="The member whose messages will be purged")
    @option("limit", int, description="Maximum messages to check", default=1000)
    async def purge_user(self, ctx: discord.ApplicationContext, member: discord.Member, limit: int):
        await ctx.defer(ephemeral=True)
        deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == member)
        await ctx.followup.send(f"✅ Deleted {len(deleted)} messages from {member.display_name}.")

    @mod.command(name="roles", description="Lists server roles and member counts")
    async def roles(self, ctx: discord.ApplicationContext):
        roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)
        embed = discord.Embed(title=f"📋 Roles in {ctx.guild.name}", color=discord.Color.blue())
        
        description = ""
        for role in roles:
            if role.is_default(): continue
            line = f"{role.mention}: {len(role.members)}\n"
            if len(description) + len(line) > 2000:
                break # Limit to avoid embed issues
            description += line
        
        embed.description = description
        await ctx.respond(embed=embed)


    @mod.command(name="sanitize_names", description="Removes non-standard characters from all nicknames")
    @commands.has_permissions(administrator=True)
    async def sanitize_names(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        standard_chars = string.ascii_letters + string.digits + string.punctuation + " "
        changed = 0
        for member in ctx.guild.members:
            sanitized = "".join(c for c in unicodedata.normalize("NFD", member.display_name) 
                               if unicodedata.category(c) != "Mn" and c in standard_chars)
            if not sanitized.strip(): sanitized = "Sanitized Name"
            if sanitized != member.display_name:
                try:
                    await member.edit(nick=sanitized)
                    changed += 1
                except: continue
        await ctx.followup.send(f"✅ Sanitized {changed} names.")

    # --- Role Group ---

    @role_grp.command(name="add_all", description="Adds a role to all members")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to add")
    async def add_role_all(self, ctx: discord.ApplicationContext, role: discord.Role):
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.respond("❌ That role is above my highest role!", ephemeral=True)
        
        await ctx.respond(f"⌛ Adding {role.name} to everyone. This will take a while...")
        count = 0
        for member in ctx.guild.members:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                    count += 1
                    await asyncio.sleep(0.5) # Prevent heavy rate limits
                except: continue
        await ctx.channel.send(f"✅ Added {role.name} to {count} members.")

    @role_grp.command(name="remove_all", description="Removes a role from all members")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to remove")
    async def remove_role_all(self, ctx: discord.ApplicationContext, role: discord.Role):
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.respond("❌ That role is above my highest role!", ephemeral=True)
        
        await ctx.respond(f"⌛ Removing {role.name} from everyone...")
        count = 0
        for member in ctx.guild.members:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    count += 1
                    await asyncio.sleep(0.5)
                except: continue
        await ctx.channel.send(f"✅ Removed {role.name} from {count} members.")

    @role_grp.command(name="clear_user", description="Removes all removable roles from a user")
    @commands.has_permissions(manage_roles=True)
    @option("member", discord.Member, description="The member to clear")
    async def clear_user_roles(self, ctx: discord.ApplicationContext, member: discord.Member):
        roles_to_remove = [r for r in member.roles if r != ctx.guild.default_role and r.position < ctx.guild.me.top_role.position]
        try:
            await member.remove_roles(*roles_to_remove)
            await ctx.respond(f"✅ Cleared {len(roles_to_remove)} roles from {member.mention}.")
        except:
            await ctx.respond("❌ Failed to remove some roles.", ephemeral=True)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """Global error handler for application commands in this cog."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(f"❌ You don't have the required permissions: `{', '.join(error.missing_permissions)}`", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(f"❌ I'm missing permissions to do that: `{', '.join(error.missing_permissions)}`", ephemeral=True)
        else:
            # For other errors, we can log them or let the global bot handler take over
            pass

def setup(bot):
    bot.add_cog(Moderation(bot))
