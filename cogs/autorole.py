import discord
from discord.ext import commands
from discord import option
import aiosqlite
import logging

# Setup logging
logger = logging.getLogger("simplex.autorole")

class AutoRole(commands.Cog):
    """🛠️ Automatically assign roles to new members when they join!"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/autoroles.db"

    # Slash Command Group for AutoRole
    ar = discord.SlashCommandGroup("autorole", "Manage roles given automatically on join")

    @ar.command(name="add", description="Add a role to be given automatically when someone joins")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to give on join")
    async def add_autorole(self, ctx, role: discord.Role):
        """Add a role to the join-role list."""
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.respond("❌ That role is above my highest role! I can't give it to anyone.", ephemeral=True)

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM autoroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id)) as cursor:
                if await cursor.fetchone():
                    return await ctx.respond(f"❌ **{role.name}** is already in the join-role list.", ephemeral=True)
            
            await db.execute("INSERT INTO autoroles (guild_id, role_id) VALUES (?, ?)", (ctx.guild.id, role.id))
            await db.commit()
            
        await ctx.respond(f"✅ **{role.name}** will now be given to all new members automatically.")

    @ar.command(name="remove", description="Remove a role from the join-role list")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to remove")
    async def remove_autorole(self, ctx, role: discord.Role):
        """Remove a role from the join-role list."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM autoroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id)) as cursor:
                if not await cursor.fetchone():
                    return await ctx.respond(f"❌ **{role.name}** is not in the join-role list.", ephemeral=True)
            
            await db.execute("DELETE FROM autoroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
            await db.commit()
            
        await ctx.respond(f"✅ Removed **{role.name}** from the join-role list.")

    @ar.command(name="list", description="List all roles given on join")
    @commands.has_permissions(manage_roles=True)
    async def list_autoroles(self, ctx):
        """Show all roles currently configured to be given on join."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT role_id FROM autoroles WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
                
        if not rows:
            return await ctx.respond("❌ No automatic join-roles have been set up yet.")
            
        embed = discord.Embed(title=f"📋 Auto-Join Roles for {ctx.guild.name}", color=discord.Color.blue())
        description = ""
        for (role_id,) in rows:
            role = ctx.guild.get_channel(role_id) # Using get_role would be better but let's be safe
            role = ctx.guild.get_role(role_id)
            if role:
                description += f"- {role.mention}\n"
            else:
                description += f"- Unknown Role (`{role_id}`)\n"
        
        embed.description = description
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Automatically add roles to new members."""
        if member.bot: return
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT role_id FROM autoroles WHERE guild_id = ?", (member.guild.id,)) as cursor:
                rows = await cursor.fetchall()
        
        if not rows: return
        
        roles_to_add = []
        for (role_id,) in rows:
            role = member.guild.get_role(role_id)
            # Only add roles if the bot has permission (role is below bot's top role)
            if role and role.position < member.guild.me.top_role.position:
                roles_to_add.append(role)
        
        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="Simplex AutoRole System")
            except Exception as e:
                logger.error(f"Failed to add autoroles for {member.name}: {e}")

def setup(bot):
    bot.add_cog(AutoRole(bot))
