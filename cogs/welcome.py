import discord
from discord.ext import commands
from discord import option
import aiosqlite
import asyncio
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import httpx
import regex
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./databases/Welcome.db"

    def generate_welcome_card(self, member_name, member_count, avatar_bytes):
        """Synchronous image generation logic, to be run in a thread."""
        with Image.open("./images/welcome.png") as background:
            avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
            avatar = avatar.resize((300, 300))
            background.paste(avatar, (1000, 200), avatar)
            
            draw = ImageDraw.Draw(background)
            try:
                font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
                font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
            except:
                font = font_small = ImageFont.load_default()
                
            draw.text((450, 550), f"Welcome {member_name}!", (255, 255, 255), font=font)
            draw.text((450, 700), f"You are the {member_count}th member!", (255, 255, 255), font=font_small)
            
            tosend = BytesIO()
            background.save(tosend, format="PNG")
            tosend.seek(0)
            return tosend

    # Slash Command Group for Welcome
    welcome_group = discord.SlashCommandGroup("welcome", "Welcome system configuration")

    @welcome_group.command(name="setup")
    @commands.has_permissions(manage_guild=True)
    @option("channel", discord.TextChannel, description="The channel to send welcome messages in")
    @option("text", str, description="The welcome message text. Use {member.mention}, {member.name}, etc.")
    @option("card", bool, description="Whether to send a welcome card image", default=False)
    @option("use_embed", bool, description="Whether to send the message as an embed", default=False)
    async def setup_welcome(self, ctx, channel: discord.TextChannel, text: str, card: bool, use_embed: bool):
        """Set up the welcome system for this server."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO welcome (guild_id, channel, text, card_enabled, textorembed, enabled) VALUES (?, ?, ?, ?, ?, 1)",
                    (ctx.guild.id, channel.id, text, 1 if card else 0, 0 if use_embed else 1)
                )
                await db.commit()
        except Exception as e:
            return await ctx.respond(f"❌ Failed to save settings: {e}", ephemeral=True)

        embed = discord.Embed(title="✅ Welcome System Configured", color=discord.Color.green())
        embed.add_field(name="Channel", value=channel.mention)
        embed.add_field(name="Card Enabled", value="Yes" if card else "No")
        embed.add_field(name="Format", value="Plain Text" if not use_embed else "Embed")
        embed.add_field(name="Message", value=text, inline=False)
        await ctx.respond(embed=embed)

    @welcome_group.command(name="toggle")
    @commands.has_permissions(manage_guild=True)
    async def toggle_welcome(self, ctx):
        """Toggle the welcome system on or off."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT enabled FROM welcome WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()
            
            if not row:
                return await ctx.respond("❌ Welcome system is not set up. Use `/welcome setup` first.")
            
            new_status = 0 if row[0] == 1 else 1
            await db.execute("UPDATE welcome SET enabled = ? WHERE guild_id = ?", (new_status, ctx.guild.id))
            await db.commit()
            
        status_text = "enabled" if new_status == 1 else "disabled"
        await ctx.respond(f"✅ Welcome system has been **{status_text}**.")

    @welcome_group.command(name="test")
    @commands.has_permissions(manage_guild=True)
    async def test_welcome(self, ctx):
        """Test the welcome system with your own profile."""
        await ctx.respond("Testing welcome message...")
        await self.on_member_join(ctx.author)

    @commands.command(name="welcome")
    @commands.has_permissions(manage_guild=True)
    async def welcome_prefix(self, ctx):
        """Show current welcome configuration."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT channel, text, card_enabled, textorembed, enabled FROM welcome WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

        if not data:
            return await ctx.send("❌ Welcome system is not set up. Use `/welcome setup` to configure it!")

        channel_id, text, card_enabled, text_mode, enabled = data
        channel = ctx.guild.get_channel(channel_id)
        
        embed = discord.Embed(title="⚙️ Welcome Configuration", color=discord.Color.blue())
        embed.add_field(name="Status", value="✅ Enabled" if enabled else "❌ Disabled")
        embed.add_field(name="Channel", value=channel.mention if channel else "None")
        embed.add_field(name="Card", value="Enabled" if card_enabled else "Disabled")
        embed.add_field(name="Format", value="Plain Text" if text_mode == 1 else "Embed")
        embed.add_field(name="Message", value=f"```{text}```" if text else "None", inline=False)
        embed.set_footer(text="Tip: Use /welcome setup to change these settings!")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot: return
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT channel, text, card_enabled, textorembed, enabled FROM welcome WHERE guild_id = ?", 
                (member.guild.id,)
            ) as cursor:
                data = await cursor.fetchone()
                
        if not data or data[4] == 0:
            return

        channel_id, text, card_enabled, text_mode, enabled = data
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return

        if card_enabled == 1:
            try:    
                async with httpx.AsyncClient() as client:
                    avatar_resp = await client.get(member.display_avatar.url)
                    avatar_bytes = avatar_resp.content
                
                # Offload blocking PIL processing to a thread
                tosend = await asyncio.to_thread(
                    self.generate_welcome_card,
                    member.name, member.guild.member_count, avatar_bytes
                )
                
                await channel.send(file=discord.File(tosend, "welcome.png"))
            except Exception as e:
                print(f"Error sending welcome card: {e}")
                
        if text:
            replacements = {
                "{member.display_name}": member.display_name,
                "{member.name}": member.name,
                "{member.mention}": member.mention,
                "{member.id}": str(member.id),
                "{member.guild.name}": member.guild.name,
                "{member.guild.member_count}": str(member.guild.member_count),
                "{member.account_age}": str(member.created_at.strftime("%Y-%m-%d")),
                "{member.joined_at}": str(member.joined_at.strftime("%Y-%m-%d")) if member.joined_at else "Unknown",
            }
            for key, val in replacements.items():
                text = text.replace(key, val)

            text = regex.sub(r"\{random\.choices\[(.+?)\]\}", lambda x: random.choice(x.group(1).split(", ")), text)

            if text_mode == 1:
                await channel.send(f"{member.mention}\n{text}")
            else:
                em = discord.Embed(title=f"Welcome to {member.guild.name}!", description=text, color=discord.Color.blue())
                em.set_thumbnail(url=member.display_avatar.url)
                await channel.send(content=member.mention, embed=em)

def setup(bot):
    bot.add_cog(Welcome(bot))
