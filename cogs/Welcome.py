import discord
from discord.ext import commands
import discord.ui
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import httpx as requests
import regex
import random

#model used to set welcome messages as futures were unreable 

class SetTextModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Set Welcome Text")
        self.view = view
        self.text_input = discord.ui.InputText(
            label="Welcome Message",
            placeholder="e.g. Welcome {member.mention} to {member.guild.name}!",
            style=discord.InputTextStyle.long
        )
        self.add_item(self.text_input)

    async def callback(self, interaction: discord.Interaction):
        text = self.text_input.value
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            await db.execute(
                "INSERT INTO welcome (guild_id, text, channel, card_enabled, textorembed, enabled) "
                "VALUES (?, ?, NULL, 0, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET text = excluded.text",
                (interaction.guild.id, text),
            )
            await db.commit()
        await interaction.response.send_message(
            embed=discord.Embed(title="Welcome Text", description=f"Set to:\n{text}"),
            ephemeral=True,
        )

#model pop up as futers became unreable on 

class SetChannelModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Set Welcome Channel")
        self.view = view
        self.channel_input = discord.ui.InputText(
            label="Channel Mention or ID",
            placeholder="#welcome or 123456789012345678",
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

        async with aiosqlite.connect("./databases/Welcome.db") as db:
            await db.execute(
                "INSERT INTO welcome (guild_id, channel, text, card_enabled, textorembed, enabled) "
                "VALUES (?, ?, NULL, 0, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET channel = excluded.channel",
                (interaction.guild.id, channel_id),
            )
            await db.commit()

        channel = interaction.guild.get_channel(channel_id) or await interaction.guild.fetch_channel(channel_id)
        await interaction.response.send_message(
            embed=discord.Embed(title="Welcome Channel", description=f"Set to {channel.mention}"),
            ephemeral=True,
        )

class ConfirmResetModal(discord.ui.Modal):
    def __init__(self, view):
        super().__init__(title="Reset Welcome Settings")
        self.view = view
        self.confirm_input = discord.ui.InputText(
            label="Type 'yes' to confirm reset",
            style=discord.InputTextStyle.short
        )
        self.add_item(self.confirm_input)

    async def callback(self, interaction: discord.Interaction):
        if self.confirm_input.value.lower() == "yes":
            async with aiosqlite.connect("./databases/Welcome.db") as db:
                await db.execute("DELETE FROM welcome WHERE guild_id = ?", (interaction.guild.id,))
                await db.commit()
            await interaction.response.send_message("Welcome settings have been reset.", ephemeral=True)
        else:
            await interaction.response.send_message("Reset cancelled.", ephemeral=True)

#Buttom menu that calles from the main cog

class WelcomeView(discord.ui.View):
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
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT enabled FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "INSERT INTO welcome (guild_id, enabled, channel, text, card_enabled, textorembed) "
                "VALUES (?, ?, NULL, NULL, 0, 0) "
                "ON CONFLICT(guild_id) DO UPDATE SET enabled = excluded.enabled",
                (self.ctx.guild.id, new_status),
            )
            await db.commit()

        await interaction.followup.send(embed=discord.Embed(title="Welcome System", description="Enabled" if new_status else "Disabled"))

    @discord.ui.button(label="Card Toggle", style=discord.ButtonStyle.green)
    async def card_toggle(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT card_enabled FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "UPDATE welcome SET card_enabled = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id)
            )
            await db.commit()

        await interaction.followup.send(embed=discord.Embed(title="Welcome Card", description="Enabled" if new_status else "Disabled"))

    @discord.ui.button(label="Text or Embed", style=discord.ButtonStyle.green)
    async def text_or_embed(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT textorembed FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

            new_status = 0 if row and row[0] else 1
            await db.execute(
                "UPDATE welcome SET textorembed = ? WHERE guild_id = ?", (new_status, self.ctx.guild.id)
            )
            await db.commit()

        desc = "Switched to Text instead of Embed" if new_status else "Switched to Embed instead of Text"
        await interaction.followup.send(embed=discord.Embed(title="Welcome Message Format", description=desc))

    @discord.ui.button(label="Show Text", style=discord.ButtonStyle.green)
    async def show_text(self, button, interaction: discord.Interaction):
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT text FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)) as cursor:
                row = await cursor.fetchone()

        if row and row[0]:
            await interaction.response.send_message(f"**Current Welcome Text:**\n{row[0]}", ephemeral=True)
        else:
            await interaction.response.send_message("No welcome text set.", ephemeral=True)

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.red)
    async def reset(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(ConfirmResetModal(self))

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx):
        view = WelcomeView(self.client, ctx)
        await ctx.send(embed=discord.Embed(title="Welcome Settings:"), view=view)
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute("SELECT * FROM welcome WHERE guild_id = ?", (member.guild.id,)) as cursor:
                data = await cursor.fetchone()
                if not data or not data[5]:
                    return
                channel_id, text, card_enabled, textorembed = data[1], data[2], data[3], data[4]

        channel = await self.client.fetch_channel(channel_id)

        if card_enabled:
            try:
                bg = Image.open("./images/welcome.png")
                avatar = Image.open(requests.get(member.display_avatar.url, stream=True).raw).resize((300, 300))
                bg.paste(avatar, (1000, 200))
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

        if not text:
            return

        replacements = {
            "{member.display_name}": member.display_name,
            "{member.name}": member.name,
            "{member.mention}": member.mention,
            "{member.id}": str(member.id),
            "{member.guild.name}": member.guild.name,
            "{member.guild.member_count}": str(member.guild.member_count),
            "{member.account_age}": str(member.created_at),
            "{member.joined_at}": str(member.joined_at),
            "{member.time_in_guild}": str(member.joined_at - member.created_at)
        }

        for key, value in replacements.items():
            text = text.replace(key, value)

        text = regex.sub(r"\{random\.choices\[(.+?)\]\}", lambda x: random.choice(x.group(1).split(", ")), text)

        if textorembed:
            await channel.send(f"{member.mention}\n{text}")
        else:
            await channel.send(embed=discord.Embed(title=f"Welcome {member.name}!", description=text), content=member.mention)

def setup(client):
    client.add_cog(Welcome(client))
