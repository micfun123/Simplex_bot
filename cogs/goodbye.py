import discord
from discord.ext import commands
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import httpx
import regex
import random

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            async with aiosqlite.connect("./databases/Goodbye.db") as db:
                async with db.execute("SELECT channel, text, card_enabled, textorembed, enabled FROM goodbye WHERE guild_id = ?", (member.guild.id,)) as cursor:
                    data = await cursor.fetchone()
            
            if not data or not data[4]: # data[4] is 'enabled'
                return
            
            channel_id, text, card_enabled, textorembed = data[0], data[1], data[2], data[3]
            channel = self.client.get_channel(channel_id) or await self.client.fetch_channel(channel_id)
            
            if card_enabled:
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(member.display_avatar.url)
                        avatar_bytes = BytesIO(resp.content)
                    
                    with Image.open("./images/goodbye.png") as bg:
                        with Image.open(avatar_bytes) as avatar:
                            avatar = avatar.convert("RGBA").resize((300, 300))
                            bg.paste(avatar, (1000, 200), avatar if avatar.mode == 'RGBA' else None)
                            draw = ImageDraw.Draw(bg)
                            font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
                            draw.text((975, 550), f"Goodbye {member.name}!", fill="white", font=font)
                            font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
                            draw.text((800, 700), f"There are now {member.guild.member_count} members!", fill="white", font=font_small)
                            
                            buf = BytesIO()
                            bg.save(buf, format="PNG")
                            buf.seek(0)
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
                }
                for key, value in replacements.items():
                    text = text.replace(key, str(value))
                
                if textorembed:
                    await channel.send(text)
                else:
                    await channel.send(embed=discord.Embed(title=f"Goodbye {member.name}!", description=text))
        except Exception as e:
            print(f"Error in on_member_remove: {e}")

def setup(client):
    client.add_cog(Goodbye(client))
