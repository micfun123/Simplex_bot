import discord
from discord.ext import commands
from discord import option
import aiosqlite
import asyncio
import logging

# Setup logging
logger = logging.getLogger("simplex.reactionroles")

class ReactionRoles(commands.Cog):
    """🛠️ Automatically assign roles or let users pick them with buttons!"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/reactionroles.db"

    # Slash Command Group for Reaction Roles
    rr = discord.SlashCommandGroup("reactionroles", "Manage automatic and button-based reaction roles")

    @rr.command(name="add", description="Add a role to the reaction roles list")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to add")
    @option("emoji", str, description="An emoji for this role (for the button menu)", default=None)
    async def add_role(self, ctx, role: discord.Role, emoji: str = None):
        """Add a role that will be given on join or shown in the menu."""
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.respond("❌ That role is above my highest role!", ephemeral=True)

        async with aiosqlite.connect(self.db_path) as db:
            # Check if already exists
            async with db.execute("SELECT * FROM reactionroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id)) as cursor:
                if await cursor.fetchone():
                    return await ctx.respond(f"❌ **{role.name}** is already in the list.", ephemeral=True)
            
            await db.execute("INSERT INTO reactionroles (guild_id, role_id, emoji) VALUES (?, ?, ?)", (ctx.guild.id, role.id, emoji))
            await db.commit()
            
        embed = discord.Embed(title="✅ Reaction Role Added", color=discord.Color.green())
        embed.description = f"**{role.name}** has been added to the system."
        if emoji:
            embed.add_field(name="Emoji", value=emoji)
        embed.set_footer(text="This role will be given on join and can be used in the /reactionroles send_menu.")
        await ctx.respond(embed=embed)

    @rr.command(name="remove", description="Remove a role from the reaction roles list")
    @commands.has_permissions(manage_roles=True)
    @option("role", discord.Role, description="The role to remove")
    async def remove_role(self, ctx, role: discord.Role):
        """Remove a role from the system."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM reactionroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id)) as cursor:
                if not await cursor.fetchone():
                    return await ctx.respond(f"❌ **{role.name}** is not in the list.", ephemeral=True)
            
            await db.execute("DELETE FROM reactionroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
            await db.commit()
            
        await ctx.respond(f"✅ Removed **{role.name}** from the reaction roles system.")

    @rr.command(name="list", description="List all reaction roles for this server")
    @commands.has_permissions(manage_roles=True)
    async def list_roles(self, ctx):
        """Show all roles currently configured."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT role_id, emoji FROM reactionroles WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
                
        if not rows:
            return await ctx.respond("❌ No reaction roles have been set up yet.")
            
        embed = discord.Embed(title=f"📋 Reaction Roles for {ctx.guild.name}", color=discord.Color.blue())
        description = ""
        for role_id, emoji in rows:
            role = ctx.guild.get_role(role_id)
            emoji_str = f"{emoji} " if emoji else ""
            if role:
                description += f"- {emoji_str}{role.mention}\n"
            else:
                description += f"- {emoji_str}Unknown Role (`{role_id}`)\n"
        
        embed.description = description
        await ctx.respond(embed=embed)

    @rr.command(name="send_menu", description="Send the button-based reaction role menu")
    @commands.has_permissions(manage_roles=True)
    @option("message", str, description="Custom message for the menu", default="Click the buttons below to pick your roles!")
    async def send_menu(self, ctx, message: str):
        """Create a button menu for self-assigning roles."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT role_id, emoji FROM reactionroles WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
                
        if not rows:
            return await ctx.respond("❌ No roles set up. Use `/reactionroles add` first.", ephemeral=True)

        view = discord.ui.View(timeout=None)
        valid_roles = 0
        
        for role_id, emoji in rows:
            role = ctx.guild.get_role(role_id)
            if not role: continue
            
            valid_roles += 1
            button = discord.ui.Button(
                label=role.name,
                style=discord.ButtonStyle.secondary,
                emoji=emoji,
                custom_id=f"rr_{role_id}"
            )
            
            async def b_callback(interaction, r_id=role_id):
                r = interaction.guild.get_role(r_id)
                if not r: return await interaction.response.send_message("Role not found.", ephemeral=True)
                if r in interaction.user.roles:
                    await interaction.user.remove_roles(r)
                    await interaction.response.send_message(f"✅ Removed **{r.name}**", ephemeral=True)
                else:
                    try:
                        await interaction.user.add_roles(r)
                        await interaction.response.send_message(f"✅ Added **{r.name}**", ephemeral=True)
                    except:
                        await interaction.response.send_message("❌ Missing permissions.", ephemeral=True)
            
            button.callback = b_callback
            view.add_item(button)

        if valid_roles == 0:
            return await ctx.respond("❌ None of the configured roles could be found.", ephemeral=True)

        embed = discord.Embed(title="🎭 Role Selection", description=message, color=discord.Color.purple())
        await ctx.channel.send(embed=embed, view=view)
        await ctx.respond("✅ Reaction role menu sent!", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Automatically add roles to new members."""
        if member.bot: return
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT role_id FROM reactionroles WHERE guild_id = ?", (member.guild.id,)) as cursor:
                rows = await cursor.fetchall()
        
        if not rows: return
        
        roles_to_add = []
        for (role_id,) in rows:
            role = member.guild.get_role(role_id)
            if role and role.position < member.guild.me.top_role.position:
                roles_to_add.append(role)
        
        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="Simplex Reaction Role System")
            except Exception as e:
                logger.error(f"Failed to add roles for {member.name}: {e}")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
