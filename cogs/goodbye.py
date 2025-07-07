import random
import regex
import textwrap
import discord
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
from discord.ext import commands
from discord import Option
import httpx as requests

#model used to set Goodbye messages as futures were unreable 

class SetTextModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Set Goodbye Text")
        self.view = view
        self.text_input = discord.ui.InputText(
            label="Goodbye Message",
            placeholder="e.g. Goodbye {member.mention} to {member.guild.name}!",
            style=discord.InputTextStyle.long
        )
        self.add_item(self.text_input)

    async def callback(self, interaction: discord.Interaction):
        text = self.text_input.value
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            await db.execute(
                "INSERT INTO Goodbye (guild_id, text, channel, card_enabled, textorembed, enabled) "
                "VALUES (?, ?, NULL, 0, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET text = excluded.text",
                (interaction.guild.id, text),
            )
            await db.commit()
        await interaction.response.send_message(
            embed=discord.Embed(title="Goodbye Text", description=f"Set to:\n{text}"),
            ephemeral=True,
        )

#model pop up as futers became unreable on 

class SetChannelModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Set Goodbye Channel")
        self.view = view
        self.channel_input = discord.ui.InputText(
            label="Channel Mention or ID",
            placeholder="#Goodbye or 123456789012345678",
            style=discord.InputTextStyle.short
        )
        self.add_item(self.channel_input)

    async def callback(self, interaction: discord.Interaction):
        content = self.channel_input.value.strip()
        try:
            if content.startswith("<#") and content.endswith(">"):
                channel_id = int(content[2:-1])
            else:
                channel_id = int(content)
        except ValueError:
            return await interaction.response.send_message("Invalid channel input.", ephemeral=True)

        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            await db.execute(
                "INSERT INTO Goodbye (guild_id, channel, text, card_enabled, textorembed, enabled) "
                "VALUES (?, ?, NULL, 0, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET channel = excluded.channel",
                (interaction.guild.id, channel_id),
            )
            await db.commit()

        channel = interaction.guild.get_channel(channel_id) or await interaction.guild.fetch_channel(channel_id)
        await interaction.response.send_message(
            embed=discord.Embed(title="Goodbye Channel", description=f"Set to {channel.mention}"),
            ephemeral=True,
        )

class ConfirmResetModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Reset Goodbye Settings")
        self.view = view
        self.confirm_input = discord.ui.InputText(
            label="Type 'yes' to confirm reset",
            style=discord.InputTextStyle.short
        )
        self.add_item(self.confirm_input)

    async def callback(self, interaction: discord.Interaction):
        if self.confirm_input.value.lower() == "yes":
            async with aiosqlite.connect("./databases/Goodbye.db") as db:
                await db.execute("DELETE FROM Goodbye WHERE guild_id = ?", (interaction.guild.id,))
                await db.commit()
            await interaction.response.send_message("Goodbye settings have been reset.", ephemeral=True)
        else:
            await interaction.response.send_message("Reset cancelled.", ephemeral=True)

#Buttom menu that calles from the main cog

class GoodbyeView(discord.ui.View):
    def __init__(self, client, ctx):
        super().__init__(timeout=30)
        self.client = client
        self.ctx = ctx

    @discord.ui.button(label="Set Text", style=discord.ButtonStyle.green)
    async def set_text(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(SetTextModal(self))

    @discord.ui.button(label="Set Channel", style=discord.ButtonStyle.green)
    async def set_channel(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(SetChannelModal(self))

    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.green)
    async def toggle(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT enabled FROM Goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "INSERT INTO Goodbye (guild_id, enabled, channel, text, card_enabled, textorembed) "
                "VALUES (?, ?, NULL, NULL, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET enabled = excluded.enabled",
                (self.ctx.guild.id, new_status),
            )
            await db.commit()

        await interaction.followup.send(embed=discord.Embed(title="Goodbye System", description="Enabled" if new_status else "Disabled"))

    @discord.ui.button(label="Card Toggle", style=discord.ButtonStyle.green)
    async def card_toggle(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT card_enabled FROM Goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "UPDATE Goodbye SET card_enabled = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id)
            )
            await db.commit()

        await interaction.followup.send(embed=discord.Embed(title="Goodbye Card", description="Enabled" if new_status else "Disabled"))

    @discord.ui.button(label="Text or Embed", style=discord.ButtonStyle.green)
    async def text_or_embed(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT textorembed FROM Goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "UPDATE Goodbye SET textorembed = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id)
            )
            await db.commit()

        desc = "Switched to Text instead of Embed" if new_status else "Switched to Embed instead of Text"
        await interaction.followup.send(embed=discord.Embed(title="Goodbye Message Format", description=desc))

    @discord.ui.button(label="Show Text", style=discord.ButtonStyle.green)
    async def show_text(self, button, interaction: discord.Interaction):
        async with aiosqlite.connect("./databases/Goodbye.db") as db:
            async with db.execute("SELECT text FROM Goodbye WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

        if row and row[0]:
            await interaction.response.send_message(f"**Current Goodbye Text:**\n{row[0]}", ephemeral=True)
        else:
            await interaction.response.send_message("No Goodbye text set.", ephemeral=True)

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.red)
    async def reset(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(ConfirmResetModal(self))

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def goodbye(self, ctx):
        view = GoodbyeView(self.client, ctx)
        embed = discord.Embed(title="Goodbye Settings")
        message = await ctx.send(embed=embed, view=view)
        await ctx.send("""
            To make welcome and bye messages more personable feel free to use these. add them to your message and the bot will auto replace them
            {member.display_name}
            {member.name}
            {member.mention}
            {member.id}
            {member.guild.name}
            {member.guild.member_count}
            {member.account_age}
            {member.joined_at}
            {member.time_in_guild}
        """)
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
