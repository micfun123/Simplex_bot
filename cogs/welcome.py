import json
from discord import Option
import discord
from discord.ext import commands
import discord.ui
import aiosqlite
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import textwrap
import regex
import random


async def get_data():
    with open("./databases/welcome.json") as f:
        data = json.load(f)
    return data


async def dump_data(data):
    with open("./databases/welcome.json", "w") as f:
        json.dump(data, f, indent=4)


class WelcomeView(discord.ui.View):
    def __init__(self, client, ctx):
        super().__init__(timeout=30)
        self.client = client
        self.ctx = ctx

    @discord.ui.button(
        label="Set Text", style=discord.ButtonStyle.green, custom_id="text"
    )
    async def set_text(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Enter the welcome text:")
        text = await self.client.wait_for("message", check=check)
        text = text.content

        async with aiosqlite.connect("./databases/Welcome.db") as db:
            # check if guild is in database
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    # if guild is not in database
                    await db.execute(
                        "INSERT INTO welcome VALUES (?,?,?,?,?,?)",
                        (self.ctx.guild.id, None, text, 0, 0, 0),
                    )
                    await db.commit()
                else:
                    # if guild is in database
                    await db.execute(
                        "UPDATE welcome SET text = ? WHERE guild_id = ?",
                        (text, self.ctx.guild.id),
                    )
                    await db.commit()

        em = discord.Embed(title="Welcome Text", description=f"Set to:\n{text}")
        await interaction.followup.send(embed=em)

    @discord.ui.button(
        label="Toggle", style=discord.ButtonStyle.green, custom_id="toggle"
    )
    async def toggle(self, button, interaction):
        data = await get_data()

        await interaction.response.edit_message(view=self)

        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    await db.execute(
                        "INSERT INTO welcome VALUES (?,?,?,?,?,?)",
                        (self.ctx.guild.id, None, None, 0, 0, 1),
                    )
                    await db.commit()
                    status = "Disabled"
                else:
                    if data[0][5] == None:
                        await db.execute(
                            "UPDATE welcome SET enabled = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Enabled"
                    elif data[0][5] == 0:
                        await db.execute(
                            "UPDATE welcome SET enabled = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Enabled"
                    else:
                        await db.execute(
                            "UPDATE welcome SET enabled = ? WHERE guild_id = ?",
                            (0, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Disabled"

        await dump_data(data)

        em = discord.Embed(title="Welcome System:", description=status)
        await interaction.followup.send(embed=em)

    @discord.ui.button(
        label="Set Channel", style=discord.ButtonStyle.green, custom_id="channel"
    )
    async def set_channel(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Enter A channel:")
        channel = await self.client.wait_for("message", check=check)
        channel = channel.content
        channel_id = int(channel[2:-1])

        async with aiosqlite.connect("./databases/Welcome.db") as db:
            # check if guild is in database
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    # if guild is not in database
                    await db.execute(
                        "INSERT INTO welcome VALUES (?,?,?,?,?,?)",
                        (self.ctx.guild.id, channel_id, None, 0, 0, 0),
                    )
                    await db.commit()
                else:
                    # if guild is in database
                    await db.execute(
                        "UPDATE welcome SET channel = ? WHERE guild_id = ?",
                        (channel_id, self.ctx.guild.id),
                    )
                    await db.commit()

        channel = await self.ctx.guild.fetch_channel(channel_id)
        em = discord.Embed(
            title="Welcome Channel", description=f"Set to {channel.mention}"
        )
        await interaction.followup.send(embed=em)

    @discord.ui.button(
        label="Card toggle", style=discord.ButtonStyle.green, custom_id="card_toggle"
    )
    async def card_toggle(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    await db.execute(
                        "INSERT INTO welcome VALUES (?,?,?,?,?,?)",
                        (self.ctx.guild.id, None, None, 0, 0, 0),
                    )
                    await db.commit()
                    status = "Disabled"
                else:
                    if data[0][3] == None:
                        await db.execute(
                            "UPDATE welcome SET card_enabled = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Enabled"
                    elif data[0][3] == 0:
                        await db.execute(
                            "UPDATE welcome SET card_enabled = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Enabled"
                    else:
                        await db.execute(
                            "UPDATE welcome SET card_enabled = ? WHERE guild_id = ?",
                            (0, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Disabled"

        em = discord.Embed(title="Welcome Card:", description=status)
        await interaction.followup.send(embed=em)

    @discord.ui.button(
        label="Text_or_Embed",
        style=discord.ButtonStyle.green,
        custom_id="text_or_embed",
    )
    async def text_or_embed(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.edit_message(view=self)
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    await db.execute(
                        "INSERT INTO welcome VALUES (?,?,?,?,?,?)",
                        (self.ctx.guild.id, None, None, 1, 0, 0),
                    )
                    await db.commit()
                    status = "Switched to Text instead of Embed"
                else:
                    if data[0][4] == None:
                        await db.execute(
                            "UPDATE welcome SET textorembed = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Switched to Text instead of Embed"
                    elif data[0][4] == 0:
                        await db.execute(
                            "UPDATE welcome SET textorembed = ? WHERE guild_id = ?",
                            (1, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Switched to Text instead of Embed"
                    else:
                        await db.execute(
                            "UPDATE welcome SET textorembed = ? WHERE guild_id = ?",
                            (0, self.ctx.guild.id),
                        )
                        await db.commit()
                        status = "Switched to Embed instead of Text"
            await interaction.followup.send(
                embed=discord.Embed(title="Welcome Text or Embed:", description=status)
            )

    @discord.ui.button(
        label="Show text", style=discord.ButtonStyle.green, custom_id="show_text"
    )
    async def show_text(self, button, interaction):
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    await interaction.response.send_message("No text set")
                else:
                    await interaction.response.send_message(data[0][2])

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.red, custom_id="reset")
    async def reset(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message(
            "Are you sure you want to reset the database? (y/n)"
        )
        res = await self.client.wait_for("message", check=check)
        res = res.content
        if res.lower() == "y":
            async with aiosqlite.connect("./databases/Welcome.db") as db:
                await db.execute(
                    "DELETE FROM welcome WHERE guild_id = ?", (self.ctx.guild.id,)
                )
                await db.commit()
                await interaction.followup.send("Your database has been reset!")
        else:
            await interaction.followup.send("Cancelled")


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx):
        view = WelcomeView(self.client, ctx)
        em = discord.Embed(title="Welcome Settings:")
        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        async with aiosqlite.connect("./databases/Welcome.db") as db:
            async with db.execute(
                "SELECT * FROM welcome WHERE guild_id = ?", (member.guild.id,)
            ) as cursor:
                data = await cursor.fetchall()
                if data == []:
                    return
                else:
                    channel = data[0][1]
                    text = data[0][2]
                    enabled = data[0][5]
                    card_enabled = data[0][3]
                    textorembed = data[0][4]

        if enabled == False:
            return

        if card_enabled == 1:
            background = Image.open("./images/welcome.png")
            avatar = Image.open(requests.get(member.avatar.url, stream=True).raw)

            avatar = avatar.resize((300, 300))
            background.paste(avatar, (1000, 200))
            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", 100)
            textlocation = (975, 200)
            textsize = draw.textsize(member.name, font=font)
            draw.text(
                (textlocation[0] - textsize[0] / 2, 550),
                f"Welcome {member.name}!",
                (255, 255, 255),
                font=font,
            )
            font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", 60)
            draw.text(
                (800, 700),
                f"You are the {member.guild.member_count}th member!",
                (255, 255, 255),
                font=font,
            )

            tosend = BytesIO()
            background.save(tosend, format="PNG")
            tosend.seek(0)
            await member.guild.get_channel(channel).send(
                file=discord.File(tosend, "welcome.png")
            )

        channel = await self.client.fetch_channel(channel)

        text = text.replace("{member.display_name}", member.display_name)
        text = text.replace("{member.name}", member.name)
        text = text.replace("{member.mention}", member.mention)
        text = text.replace("{member.id}", str(member.id))
        text = text.replace("{member.guild.name}", member.guild.name)
        text = text.replace(
            "{member.guild.member_count}", str(member.guild.member_count)
        )
        text = text.replace("{member.account_age}", str(member.created_at))
        text = text.replace("{member.joined_at}", str(member.joined_at))
        text = text.replace(
            "{member.time_in_guild}", str(member.joined_at - member.created_at)
        )
        # replace {random.choices[usersinput seperated by comma]}
        text = regex.sub(
            r"\{random\.choices\[(.+?)\]\}",
            lambda x: random.choice(x.group(1).split(", ")),
            text,
        )
        # example: {random.choices[hi, hello, hey, hola]}
        em = discord.Embed(title=f"Welcome {member.name}!", description=text)
        if textorembed == 1:
            await channel.send(f"{member.mention} \n {text}")
        else:
            await channel.send(embed=em, content=member.mention)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = await get_data()

        append_this = {
            "guild_id": guild.id,
            "channel": None,
            "text": None,
            "enabled": False,
        }
        data.append(append_this)

        await dump_data(data)


def setup(client):
    client.add_cog(Welcome(client))
