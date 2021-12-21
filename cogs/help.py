import discord
import json
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add_help(self, ctx):
        dev_ids = [624076054969188363, 481377376475938826]

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        with open("help.json") as f:
            data = json.load(f)
            
        if ctx.author.id in dev_ids:

            await ctx.send(embed=discord.Embed(title="Please enter the command name:"))
            name = await self.client.wait_for("message", check=check)
            name = str(name.content)

            for cmd in data:
                if cmd['name'] == name:
                    await ctx.send("This command already exists")
                    return

            await ctx.send(embed=discord.Embed(title="Please enter the description:"))
            desc = await self.client.wait_for("message", check=check)
            desc = str(desc.content)

            await ctx.send(embed=discord.Embed(title="Please enter the usage:"))
            use = await self.client.wait_for("message", check=check)
            use = str(use.content)
            help_command = {
                "name": name,
                "description": desc,
                "usage": f"`{use}`"
            }

            data.append(help_command)
            with open('help.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            await ctx.send(f"Command created successfully. You can view it using `.help {name}`")

        else:
            await ctx.send("You dont have permission to use this command")

    @commands.command()
    async def help(self, ctx, command=None):
        with open('help.json') as f:
            data = json.load(f)

        if command == None:
            em = discord.Embed(title="Simplex Help:", description="Use `.help <command>` for more info on command")
            for i in data:
                em.add_field(name=i['name'], value=i["description"], inline=False)
                await ctx.send(embed=em)
                return
        else:
            for i in data:
                if i["name"] == command:
                    em = discord.Embed(title="Simplex Help:", description="Use `.help <command>` for more info on command")
                    em.add_field(name="Name: ", value=i["name"])
                    em.add_field(name="Description: ", value=i["description"])
                    em.add_field(name="Usage: ", value=i["usage"])

                    await ctx.send(embed=em)
                    return
            await ctx.send(embed=discord.Embed(title="Simplex Help:", description="Command not found. Use `.help` for a list of commands"))


def setup(client):
    client.add_cog(Help(client))