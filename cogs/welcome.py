import json
from discord import Option
import discord
from discord.ext import commands
import discord.ui


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


    @discord.ui.button(label="Set Text", style=discord.ButtonStyle.green, custom_id="text")
    async def set_text(self, button, interaction):
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Enter the welcome text:")
        text = await self.client.wait_for("message", check=check)
        text = text.content

        data = await get_data()

        for i in data:
            if i['guild_id'] == self.ctx.guild.id:
                i['text'] = text

        await dump_data(data)

        em = discord.Embed(title="Welcome Text",
                           description=f"Set to:\n{text}")
        await interaction.followup.send(embed=em)


    @discord.ui.button(label="Toggle", style=discord.ButtonStyle.green, custom_id="toggle")
    async def toggle(self, button, interaction):

        data = await get_data()

        await interaction.response.edit_message(view=self)

        for guild in data:
            if guild['guild_id'] == self.ctx.guild.id:
                if guild['enabled'] == False:
                    guild['enabled'] = True
                    status = "Enabled ✅"
                elif guild['enabled'] == True:
                    guild['enabled'] = False
                    status = "Disabled ❌"

        await dump_data(data)

        em = discord.Embed(title="Welcome System:", description=status)
        await interaction.followup.send(embed=em)


    @discord.ui.button(label="Set Channel", style=discord.ButtonStyle.green, custom_id="channel")
    async def set_channel(self, button, interaction):

        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author

        await interaction.response.send_message("Enter the channel ID")
        channel_id = await self.client.wait_for("message", check=check)
        channel_id = int(channel_id.content)

        data = await get_data()
        for i in data:
            if i['guild_id'] == self.ctx.guild.id:
                i['channel'] = channel_id

        await dump_data(data)

        channel = await self.ctx.guild.fetch_channel(channel_id)
        em = discord.Embed(title="Welcome Channel",
                           description=f"Set to {channel.mention}")
        await interaction.followup.send(embed=em)


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


    # Once again, this command should not be anywhere anymore.
    # - EpicPix
    #
    # @commands.command()
    # async def set_all(self, ctx):
    #     data = await get_data()
    #     for guild in self.client.guilds:
    #         append_this = {
    #             "guild_id": guild.id,
    #             "channel": None,
    #             "text": None,
    #             "enabled": False
    #         }
    #         data.append(append_this)
    #
    #     await dump_data(data)
    #     await ctx.send("Done")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = await get_data()
        for i in data:
            if i['guild_id'] == member.guild.id:
                stuff = i

        channel = stuff['channel']
        text = stuff['text']
        enabled = stuff['enabled']

        if enabled == False:
            return

        channel = await self.client.fetch_channel(channel)

        em = discord.Embed(title=f"Welcome {member.name}!", description=text)
        await channel.send(embed=em, content=member.mention)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = await get_data()

        append_this = {
            "guild_id": guild.id,
            "channel": None,
            "text": None,
            "enabled": False
        }
        data.append(append_this)

        await dump_data(data)


def setup(client):
    client.add_cog(Welcome(client))
