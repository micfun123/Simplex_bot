import random
import regex
import requests
import textwrap
import discord
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
from discord.ext import commands
from discord import Option

class GoodbyeView(discord.ui.View):
    def __init__(self, client, ctx):
        super().__init__(timeout=30)
        self.client = client
        self.ctx = ctx

    @discord.ui.button(label="Set Text", style=discord.ButtonStyle.green, custom_id="text")
    async def set_text(self, button, interaction):
        def check(m): return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Enter the goodbye text:")
        msg = await self.client.wait_for("message", check=check)
        text = msg.content

        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

            if not data:
                await db.execute(
                    "INSERT INTO goodbye VALUES (?,?,?,?,?,?)",
                    (self.ctx.guild.id, None, text, 0, 0, 0)
                )
            else:
                await db.execute(
                    "UPDATE goodbye SET text = ? WHERE guild_id = ?",
                    (text, self.ctx.guild.id)
                )
            await db.commit()

        embed = discord.Embed(title="Goodbye Text", description=f"Set to:\n{text}")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.green, custom_id="toggle")
    async def toggle(self, button, interaction):
        await interaction.response.edit_message(view=self)

        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

            if not data:
                await db.execute("INSERT INTO goodbye VALUES (?,?,?,?,?,?)", (self.ctx.guild.id, None, None, 0, 0, 1))
                status = "Disabled"
            else:
                new_status = 0 if data[5] else 1
                await db.execute("UPDATE goodbye SET enabled = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id))
                status = "Enabled" if new_status else "Disabled"
            await db.commit()

        embed = discord.Embed(title="Goodbye System", description=status)
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Set Channel", style=discord.ButtonStyle.green, custom_id="channel")
    async def set_channel(self, button, interaction):
        def check(m): return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Mention a channel:")
        msg = await self.client.wait_for("message", check=check)
        try:
            channel_id = int(msg.content.strip("<>#").replace("<#", "").replace(">", ""))
            channel = await self.ctx.guild.fetch_channel(channel_id)
        except Exception:
            return await interaction.followup.send("Invalid channel format.")

        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

            if not data:
                await db.execute("INSERT INTO goodbye VALUES (?,?,?,?,?,?)", (self.ctx.guild.id, channel_id, None, 0, 0, 0))
            else:
                await db.execute("UPDATE goodbye SET channel = ? WHERE guild_id = ?", (channel_id, self.ctx.guild.id))
            await db.commit()

        embed = discord.Embed(title="Goodbye Channel", description=f"Set to {channel.mention}")
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Card Toggle", style=discord.ButtonStyle.green, custom_id="card_toggle")
    async def card_toggle(self, button, interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

            new_status = 0 if data and data[3] else 1
            if not data:
                await db.execute("INSERT INTO goodbye VALUES (?,?,?,?,?,?)", (self.ctx.guild.id, None, None, 1, 0, 0))
            else:
                await db.execute("UPDATE goodbye SET card_enabled = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id))
            await db.commit()

        status = "Enabled" if new_status else "Disabled"
        await interaction.followup.send(embed=discord.Embed(title="Goodbye Card", description=status))

    @discord.ui.button(label="Text or Embed", style=discord.ButtonStyle.green, custom_id="text_or_embed")
    async def text_or_embed(self, button, interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()

            new_status = 0 if data and data[4] else 1
            if not data:
                await db.execute("INSERT INTO goodbye VALUES (?,?,?,?,?,?)", (self.ctx.guild.id, None, None, 0, new_status, 0))
            else:
                await db.execute("UPDATE goodbye SET textorembed = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id))
            await db.commit()

        desc = "Switched to Text" if new_status else "Switched to Embed"
        await interaction.followup.send(embed=discord.Embed(title="Goodbye Format", description=desc))

    @discord.ui.button(label="Show Text", style=discord.ButtonStyle.green, custom_id="show_text")
    async def show_text(self, button, interaction):
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                data = await cursor.fetchone()
                if not data:
                    await interaction.response.send_message("No text set.")
                else:
                    await interaction.response.send_message(data[2])

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.red, custom_id="reset")
    async def reset(self, button, interaction):
        def check(m): return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Are you sure you want to reset the database? (y/n)")
        msg = await self.client.wait_for("message", check=check)
        if msg.content.lower() == "y":
            async with aiosqlite.connect("./databases/Goodbye.db") as db:
                await db.execute("DELETE FROM goodbye WHERE guild_id = ?", (self.ctx.guild.id,))
                await db.commit()
            await interaction.followup.send("Database reset.")
        else:
            await interaction.followup.send("Cancelled.")


class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def goodbye(self, ctx):
        view = GoodbyeView(self.client, ctx)
        embed = discord.Embed(title="Goodbye Settings")
        message = await ctx.send(embed=embed, view=view)
        await view.wait()
        for item in view.children:
            item.disabled = True
        await message.edit(view=view)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT * FROM goodbye WHERE guild_id = ?", (member.guild.id,)) as cursor:
                data = await cursor.fetchone()

        if not data or not data[5]:
            return

        channel_id, text, card_enabled, textorembed = data[1], data[2], data[3], data[4]
        channel = await self.client.fetch_channel(channel_id)

        if card_enabled:
            try:
                bg = Image.open("./images/goodbye.png")
                avatar = Image.open(requests.get(member.avatar.url, stream=True).raw).resize((300, 300))
                bg.paste(avatar, (1000, 200))

                draw = ImageDraw.Draw(bg)
                font_main = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
                font_small = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)

                draw.text((975, 550), f"Goodbye {member.name}!", (255, 255, 255), font=font_main)
                draw.text((800, 700), f"There are now {member.guild.member_count} members!", (255, 255, 255), font=font_small)

                buffer = BytesIO()
                bg.save(buffer, format="PNG")
                buffer.seek(0)

                await channel.send(file=discord.File(buffer, "goodbye.png"))
            except Exception:
                pass

        if not text:
            return

        time_in_server = datetime.now(timezone.utc) - member.joined_at.replace(tzinfo=timezone.utc)
        replacements = {
            "{member.display_name}": member.display_name,
            "{member.name}": member.name,
            "{member.mention}": member.mention,
            "{member.id}": str(member.id),
            "{member.guild.name}": member.guild.name,
            "{member.guild.member_count}": str(member.guild.member_count),
            "{member.account_age}": str(member.created_at),
            "{member.joined_at}": str(member.joined_at),
            "{member.time_in_guild}": f"{time_in_server.days}d {time_in_server.seconds // 3600}h {time_in_server.seconds // 60 % 60}m",
            "{member.top_role}": member.top_role.name,
            "{member.roles}": ", ".join(role.name for role in member.roles),
            "{member.guild.owner}": member.guild.owner.name
        }

        for key, val in replacements.items():
            text = text.replace(key, val)

        text = regex.sub(r"\{random\.choices\[(.+?)\]\}", lambda m: random.choice(m.group(1).split(", ")), text)

        if textorembed:
            await channel.send(text)
        else:
            embed = discord.Embed(title=f"Goodbye {member.name}!", description=text)
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(Goodbye(client))
