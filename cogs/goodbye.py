import discord
from discord.ext import commands
from discord import option
import aiosqlite
import asyncio
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import httpx
import re as regex
import random

class Goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./databases/Goodbye.db"

    def generate_goodbye_card(self, member_name, member_count, avatar_bytes):
        """Synchronous image generation logic, to be run in a thread."""
        with Image.open("./images/goodbye.png") as bg:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                avatar = avatar.convert("RGBA").resize((300, 300))
                bg.paste(avatar, (1000, 200), avatar)
                draw = ImageDraw.Draw(bg)
                try:
                    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
                    font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
                except:
                    font = font_small = ImageFont.load_default()
                    
                draw.text((450, 550), f"Goodbye {member_name}!", fill="white", font=font)
                draw.text((450, 700), f"There are now {member_count} members!", fill="white", font=font_small)
                
                buf = BytesIO()
                bg.save(buf, format="PNG")
                buf.seek(0)
                return buf

    # Slash Command Group for Goodbye
    goodbye = discord.SlashCommandGroup("goodbye", "Goodbye system configuration")

    @goodbye.command(name="setup")
    @commands.has_permissions(manage_guild=True)
    @option("channel", discord.TextChannel, description="The channel to send goodbye messages in")
    @option("text", str, description="The goodbye message text. Use {member.mention}, {member.name}, etc.")
    @option("card", bool, description="Whether to send a goodbye card image", default=False)
    @option("use_embed", bool, description="Whether to send the message as an embed", default=False)
    async def setup_goodbye(self, ctx, channel: discord.TextChannel, text: str, card: bool, use_embed: bool):
        """Set up the goodbye system for this server."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO goodbye (guild_id, channel, text, card_enabled, textorembed, enabled)
                VALUES (?, ?, ?, ?, ?, 1)
                ON CONFLICT(guild_id) DO UPDATE SET 
                    channel = EXCLUDED.channel,
                    text = EXCLUDED.text,
                    card_enabled = EXCLUDED.card_enabled,
                    textorembed = EXCLUDED.textorembed,
                    enabled = 1
            """, (ctx.guild.id, channel.id, text, 1 if card else 0, 1 if use_embed else 0)) # Note: db uses 1 for embed in current logic for goodbye? let's stick to consistent logic
            await db.commit()
        
        embed = discord.Embed(title="✅ Goodbye System Configured", color=discord.Color.red())
        embed.add_field(name="Channel", value=channel.mention)
        embed.add_field(name="Card Enabled", value="Yes" if card else "No")
        embed.add_field(name="Format", value="Plain Text" if not use_embed else "Embed")
        embed.add_field(name="Message", value=text, inline=False)
        await ctx.respond(embed=embed)

    @goodbye.command(name="toggle")
    @commands.has_permissions(manage_guild=True)
    async def toggle_goodbye(self, ctx):
        """Toggle the goodbye system on or off."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT enabled FROM goodbye WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()
            
            if not row:
                return await ctx.respond("❌ Goodbye system is not set up. Use `/goodbye setup` first.")
            
            new_status = 0 if row[0] == 1 else 1
            await db.execute("UPDATE goodbye SET enabled = ? WHERE guild_id = ?", (new_status, ctx.guild.id))
            await db.commit()
            
        status_text = "enabled" if new_status == 1 else "disabled"
        await ctx.respond(f"✅ Goodbye system has been **{status_text}**.")

    @goodbye.command(name="test")
    @commands.has_permissions(manage_guild=True)
    async def test_goodbye(self, ctx):
        """Test the goodbye system with your own profile."""
        await ctx.respond("Testing goodbye message...")
        await self.on_member_remove(ctx.author)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("SELECT channel, text, card_enabled, textorembed, enabled FROM goodbye WHERE guild_id = ?", (member.guild.id,)) as cursor:
                    data = await cursor.fetchone()
            
            if not data or not data[4]: # enabled check
                return
            
            channel_id, text, card_enabled, textorembed = data[0], data[1], data[2], data[3]
            channel = member.guild.get_channel(channel_id)
            if not channel:
                return
            
            if card_enabled:
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(member.display_avatar.url)
                        avatar_bytes = resp.content
                    
                    # Offload blocking PIL processing to a thread
                    buf = await asyncio.to_thread(
                        self.generate_goodbye_card,
                        member.name, member.guild.member_count, avatar_bytes
                    )
                    
                    await channel.send(file=discord.File(buf, "goodbye.png"))
                except Exception as e:
                    print(f"[Goodbye Card Error] {e}")

            if text:
                replacements = {
                    "{member.display_name}": member.display_name,
                    "{member.name}": member.name,
                    "{member.mention}": member.mention,
                    "{member.id}": str(member.id),
                    "{member.guild.name}": member.guild.name,
                    "{member.guild.member_count}": str(member.guild.member_count),
                    "{member.time_in_guild}": str((discord.utils.utcnow() - member.joined_at).days) + " days" if member.joined_at else "Unknown",
                    "{member.joined_at}": str(member.joined_at.strftime("%Y-%m-%d")) if member.joined_at else "Unknown"
                }
                for key, value in replacements.items():
                    text = text.replace(key, str(value))

                text = regex.sub(r"\{random\.choices\[(.+?)\]\}", lambda x: random.choice(x.group(1).split(", ")), text)


                
                if not textorembed: # Plain Text
                    await channel.send(text)
                else: # Embed
                    await channel.send(embed=discord.Embed(title=f"Goodbye {member.name}!", description=text, color=discord.Color.orange()))
        except Exception as e:
            print(f"Error in on_member_remove: {e}")

def setup(bot):
    bot.add_cog(Goodbye(bot))
