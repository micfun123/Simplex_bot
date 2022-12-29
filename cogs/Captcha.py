import discord
from discord.ext import commands
import asyncio
import aiosqlite


class verificationview(discord.ui.View):
    def __init__(self, client, ctx):
        super().__init__(timeout=30)
        self.client = client
        self.ctx = ctx

    @discord.ui.button(label="toggle", style=discord.ButtonStyle.green, custom_id="toggle")
    async def toggle(self, button, interaction):
        async with aiosqlite.connect("databases/verification.db") as db:
            data = await db.execute("SELECT * FROM verification WHERE ServerID = ?", (self.ctx.guild.id,))
            data = await data.fetchall()
            if data: 
                if data[0][1] == 0:
                    await db.execute("UPDATE verification SET ServerToggle = 1 WHERE ServerID = ?", (self.ctx.guild.id,))
                    await db.commit()
                    await db.close()
                    await interaction.response.send_message("verification is now enabled")
                elif data[0][1] == 1:
                    await db.execute("UPDATE verification SET ServerToggle = 0 WHERE ServerID = ?", (self.ctx.guild.id,))
                    await db.commit()
                    await db.close()
                    await interaction.response.send_message("verification is now disabled")
            else:
                await db.execute("INSERT INTO verification VALUES(?, ?, ?, ?, ?)", (self.ctx.guild.id, 1, 0, 0, 0))
                await db.commit()
                await db.close()
                await interaction.response.send_message("verification is now enabled")

    @discord.ui.button(label="set channel", style=discord.ButtonStyle.green, custom_id="set channel")
    async def set_channel(self, button, interaction):
        await interaction.response.send_message("Enter the channel")
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author
        channel = await self.client.wait_for("message", check=check)
        channel = channel.content
        channel = self.ctx.guild.get_channel(int(channel[2:-1]))
        async with aiosqlite.connect("databases/verification.db") as db:
            data = await db.execute("SELECT * FROM verification WHERE ServerID = ?", (self.ctx.guild.id,))
            data = await data.fetchall()
            if data:
                await db.execute("UPDATE verification SET verifyChannel = ? WHERE ServerID = ?", (channel.id, self.ctx.guild.id))
                await db.commit()
                await db.close()
                await interaction.followup.send(f"verification channel is now {channel.mention}")
            else:
                await db.execute("INSERT INTO verification VALUES(?, ?, ?, ?, ?)", (self.ctx.guild.id, 0, channel.id, 0, 0))
                await db.commit()
                await db.close()
                await interaction.followup.send(f"verification channel is now {channel.mention}")

    @discord.ui.button(label="set code", style=discord.ButtonStyle.green, custom_id="set code")
    async def set_code(self, button, interaction):
        await interaction.response.send_message("Enter the code")
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author
        code = await self.client.wait_for("message", check=check)
        code = code.content
        async with aiosqlite.connect("databases/verification.db") as db:
            data = await db.execute("SELECT * FROM verification WHERE ServerID = ?", (self.ctx.guild.id,))
            data = await data.fetchall()
            if data:
                await db.execute("UPDATE verification SET verifycode = ? WHERE ServerID = ?", (code, self.ctx.guild.id))
                await db.commit()
                await db.close()
                await interaction.followup.send(f"verification code is now {code}")
            else:
                await db.execute("INSERT INTO verification VALUES(?, ?, ?, ?, ?)", (self.ctx.guild.id, 0, 0, code, 0))
                await db.commit()
                await db.close()
                await interaction.followup.send(f"verification code is now {code}")

    @discord.ui.button(label="set role", style=discord.ButtonStyle.green, custom_id="set role")
    async def set_role(self, button, interaction):
        await interaction.response.send_message("Enter the role")
        def check(m):
            return m.channel == self.ctx.channel and m.author == self.ctx.author
        role = await self.client.wait_for("message", check=check)
        role = role.content
        #if role is above the bot
        if self.ctx.guild.me.top_role.position < self.ctx.guild.get_role(int(role[3:-1])).position:
            await interaction.followup.send("The role is above the bot")
        else:
            role = self.ctx.guild.get_role(int(role[3:-1]))
            async with aiosqlite.connect("databases/verification.db") as db:
                data = await db.execute("SELECT * FROM verification WHERE ServerID = ?", (self.ctx.guild.id,))
                data = await data.fetchall()
                if data:
                    await db.execute("UPDATE verification SET verifyedRole = ? WHERE ServerID = ?", (role.id, self.ctx.guild.id))
                    await db.commit()
                    await db.close()
                    await interaction.followup.send(f"verification role is now {role.mention}")
                else:
                    await db.execute("INSERT INTO verification VALUES(?, ?, ?, ?, ?)", (self.ctx.guild.id, 0, 0, 0, role.id))
                    await db.commit()
                    await db.close()
                    await interaction.followup.send(f"verification role is now {role.mention}")



class Captcha(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def verification(self, ctx):
        view = verificationview(self.client, ctx)
        em = discord.Embed(title="verification Settings:")
        message = await ctx.send(embed=em, view=view)
        res = await view.wait()
        if res:
            for i in view.children:
                i.disabled = True
        return await message.edit(view=view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        async with aiosqlite.connect("databases/verification.db") as db:
            data = await db.execute("SELECT * FROM verification WHERE ServerID = ?", (message.guild.id,))
            data = await data.fetchall()
            if data:
                if data[0][1] == 1:
                    if data[0][2] == message.channel.id:
                        if data[0][3] == message.content:
                            await message.author.add_roles(message.guild.get_role(data[0][4]))
                            await message.delete()
                            await message.channel.send(f"Welcome to {message.guild.name} {message.author.mention}")
                        else:
                            await message.delete()
                            #dm user that he entered the wrong code
                            await message.author.send("You entered the wrong verification code on {message.guild.name}")
                else:
                    return
            else:
                return
    
    @commands.command()
    @commands.is_owner()
    async def maketableverification(self, ctx):
        async with aiosqlite.connect("databases/verification.db") as db:
            await db.execute("CREATE TABLE verification(ServerID int, ServerToggle, verifyChannel int, verifycode int, verifyedRole int)")
            await db.commit()
            await db.close()


def setup(client):
    client.add_cog(Captcha(client))