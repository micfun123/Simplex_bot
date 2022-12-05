import discord
import json
from discord.ext import commands
from datetime import datetime
import aiosqlite

class Autorole(commands.Cog):
    def __init__(self, client):
        self.client = client

    #@commands.command()
    #@commands.is_owner()
    #async def make_tabe(self, ctx,):
    #    async with aiosqlite.connect("databases/autoroles.db") as db:
    #        await db.execute("CREATE TABLE IF NOT EXISTS autoroles (guild_id int, role_id int)")
    #        await db.commit()
    #        await ctx.send("Table created")


    @commands.slash_command(name="add_autorole")
    @commands.has_permissions(administrator=True)
    async def add_autoroles__slashcommand(self,ctx, role : discord.Role):
        #if role is above the bot's highest role
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("The role is above my highest role")
        roleid = role.id
        guildid = ctx.guild.id
        try:
            async with aiosqlite.connect("databases/autoroles.db") as db:
                await db.execute("INSERT INTO autoroles VALUES (?,?)", (guildid, roleid))
                await db.commit()
            await ctx.respond(f"Added {role} to autoroles")
        except:
            ctx.respond("Failed for unknown reason")

    @commands.slash_command(name="remove_autorole")
    @commands.has_permissions(administrator=True)
    async def remove_autoroles__slashcommand(self,ctx, role: discord.Role):
        async with aiosqlite.connect("databases/autoroles.db") as db:
            await db.execute("DELETE FROM autoroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
            await db.commit()
        await ctx.respond(f"Removed {role.name} from autoroles")



    @commands.command(name="add_autorole")
    @commands.has_permissions(administrator=True)
    async def add_autoroles__command(self,ctx, role : discord.Role):
        #if role is above the bot's highest role
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("The role is above my highest role")
        roleid = role.id
        guildid = ctx.guild.id
        async with aiosqlite.connect("databases/autoroles.db") as db:
            await db.execute("INSERT INTO autoroles VALUES (?,?)", (guildid, roleid))
            await db.commit()
        await ctx.send(f"Added {role} to autoroles")

    @commands.command(name="remove_autorole")
    @commands.has_permissions(administrator=True)
    async def remove_autoroles__command(self,ctx, role: discord.Role):
        async with aiosqlite.connect("databases/autoroles.db") as db:
            await db.execute("DELETE FROM autoroles WHERE guild_id = ? AND role_id = ?", (ctx.guild.id, role.id))
            await db.commit()
        await ctx.send(f"Removed {role.name} from autoroles")

    @commands.command(name="list_autoroles")
    @commands.has_permissions(administrator=True)
    async def list_autoroles_commands(self,ctx):
        async with aiosqlite.connect("databases/autoroles.db") as db:
            cursor = await db.execute("SELECT role_id FROM autoroles WHERE guild_id = ?", (ctx.guild.id,))
            roles = await cursor.fetchall()
        if not roles:
            return await ctx.send("No autoroles set")
        role_names = [ctx.guild.get_role(role[0]).name for role in roles]
        await ctx.send("Autoroles: " + ", ".join(role_names))

    @commands.slash_command(name="list_autoroles")
    @commands.has_permissions(administrator=True)
    async def list_autoroles_slash(self,ctx):
        async with aiosqlite.connect("databases/autoroles.db") as db:
            cursor = await db.execute("SELECT role_id FROM autoroles WHERE guild_id = ?", (ctx.guild.id,))
            roles = await cursor.fetchall()
        if not roles:
            return await ctx.respond("No autoroles set")
        role_names = [ctx.guild.get_role(role[0]).name for role in roles]
        await ctx.respond("Autoroles: " + ", ".join(role_names))

    #@commands.is_owner()
    #@commands.command()
    #async def json_to_sql(self, ctx):
    #    with open("databases/autorole.json", "r") as f:
    #        data = json.load(f)
    #    async with aiosqlite.connect("databases/autoroles.db") as db:
    #        for i in data:
    #            await db.execute("INSERT INTO autoroles VALUES (?,?)", (i, data[i]))
    #            await db.commit()
    #    await ctx.send("Done")
        

    #@commands.command(help="Sets the autorole for the server")
    #@commands.has_permissions(administrator=True)
    #async def autorole(self, ctx, role:discord.Role):
    #    role_id = role.id
    #    guild_id = str(ctx.guild.id)
#
    #    with open("./databases/autorole.json") as f:
    #        data = json.load(f)
#
    #    data[guild_id] = role_id
    #    
    #    with open("./databases/autorole.json", 'w') as f:
    #        json.dump(data, f, indent=4)
#
    #    await ctx.send(embed=discord.Embed(title=f"{role.mention} has been set as the autorole for this server"))
#
    #@commands.command()
    #@commands.has_permissions(administrator=True)
    #async def autorolereset(self, ctx):
    #    guild_id = str(ctx.guild.id)
#
    #    with open("./databases/autorole.json") as f:
    #        data = json.load(f)
#
    #    data[guild_id] = None
    #    
    #    with open("./databases/autorole.json", 'w') as f:
    #        json.dump(data, f, indent=4)
#
    #    await ctx.send(embed=discord.Embed(title="Autorole reset"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        async with aiosqlite.connect("databases/autoroles.db") as db:
            cursor = await db.execute("SELECT role_id FROM autoroles WHERE guild_id = ?", (member.guild.id,))
            roles = await cursor.fetchall()
        if roles is None:
            return
        else:
            for role in roles:
                await member.add_roles(member.guild.get_role(role[0]))
        

       




def setup(client):
    client.add_cog(Autorole(client))