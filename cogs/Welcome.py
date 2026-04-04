import discord
from discord.ext import commands
import discord.ui
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import httpx
import regex
import random

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            async with aiosqlite.connect("./databases/Welcome.db") as db:
                async with db.execute("SELECT channel, text, card_enabled, textorembed, enabled FROM welcome WHERE guild_id = ?", (member.guild.id,)) as cursor:
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
                    
                    with Image.open("./images/welcome.png") as bg:
                        with Image.open(avatar_bytes) as avatar:
                            avatar = avatar.convert("RGBA").resize((300, 300))
                            bg.paste(avatar, (1000, 200), avatar if avatar.mode == 'RGBA' else None)
                            draw = ImageDraw.Draw(bg)
                            font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
                            draw.text((975, 550), f"Welcome {member.name}!", fill="white", font=font)
                            font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
                            draw.text((800, 700), f"You are the {member.guild.member_count}th member!", fill="white", font=font_small)
                            
                            buf = BytesIO()
                            bg.save(buf, format="PNG")
                            buf.seek(0)
                            await channel.send(file=discord.File(buf, "welcome.png"))
                except Exception as e:
                    print(f"[Welcome Card Error] {e}")

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
                    await channel.send(f"{member.mention}\n{text}")
                else:
                    await channel.send(embed=discord.Embed(title=f"Welcome {member.name}!", description=text), content=member.mention)
        except Exception as e:
            print(f"Error in on_member_join: {e}")

def setup(client):
    client.add_cog(Welcome(client))
