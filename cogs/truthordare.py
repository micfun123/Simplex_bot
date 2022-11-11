import discord
from discord.ext import commands 
from discord.ui import Button , View
import sqlite3
import random

betaservers = [908963077125459989,401041820458680340,985655459576959078]

# Somewhere (in the check func)


def enabled_check(ctx):
    con = sqlite3.connect('databases/truthordare.db')
    cur = con.cursor()
    cur.execute(f"SELECT toggel FROM truthordare WHERE server_id = {ctx.guild.id}")
    result = cur.fetchone()
    if result[0] == 1:
        return True
    else:
        return False

def get_truth():
    with open("databases/truth.txt", "r") as f:
            lines = f.readlines()
    embed = discord.Embed(title="Truth", description=random.choice(lines), color=0x00ff00)
    return embed

def get_dare():
    with open("databases/dare.txt", "r") as f:
            lines = f.readlines()
    embed = discord.Embed(title="Dare", description=random.choice(lines), color=0xFF0000)
    return embed

def get_random_truthordare():
    random_number = random.randint(1, 2)
    if random_number == 1:
        return get_truth()
    else:
        return get_dare()
class TruthOrDare(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def maketable(self, ctx):
        con = sqlite3.connect('databases/truthordare.db')
        cur = con.cursor()
        cur.execute("CREATE table truthordare (server_id int, toggel int)")
        con.commit()
        con.close()
        await ctx.send("Table created")
        for i in self.client.guilds:
            con = sqlite3.connect('databases/truthordare.db')
            cur = con.cursor()
            cur.execute("INSERT INTO truthordare VALUES (?, ?)", (i.id, 0))
            con.commit()
            con.close()
        await ctx.send("Table filled")
    
    #onserverjoin
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        con = sqlite3.connect('databases/truthordare.db')
        cur = con.cursor()
        data = cur.execute("SELECT * FROM truthordare WHERE server_id = ?", (guild.id,))
        data = data.fetchall()
        if len(data) == 0:
            cur.execute("INSERT INTO truthordare VALUES (?, ?)", (guild.id, 0))
            con.commit()
            con.close()
        else:
            pass

    @commands.slash_command(name="toggle_truthordare", description="Toggle truth or dare",server_ids=betaservers)
    @commands.has_permissions(administrator=True)
    async def truthordare_toggle(self, ctx):
        con = sqlite3.connect('databases/truthordare.db')
        cur = con.cursor()
        data = cur.execute("SELECT toggel FROM truthordare WHERE server_id = ?", (ctx.guild.id,))
        data = data.fetchall()
        #check if there is a row for the server
        if len(data):
            if data[0][0] == 0:
                cur.execute("UPDATE truthordare SET toggel = ? WHERE server_id = ?", (1, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("Truth or dare enabled!")
            else:
                cur.execute("UPDATE truthordare SET toggel = ? WHERE server_id = ?", (0, ctx.guild.id))
                con.commit()
                con.close()
                await ctx.respond("Truth or dare disabled!")
        else:
            cur.execute("INSERT INTO truthordare VALUES (?, ?)", (ctx.guild.id, 1))
            con.commit()
            con.close()
            await ctx.respond("Truth or dare enabled!")
        await ctx.respond("Please feel free to vote for simplex and me. It would mean a lot to us and it helps load. https://top.gg/bot/902240397273743361", ephemeral=True)

    @commands.command()
    @commands.is_owner()
    async def maketruthfile(self, ctx):
        #wipe file
        open("databases/dare.txt", "w").close()
        truthfile = open("databases/truth.txt", "w")
        channel = self.client.get_channel(1031279120623083560)
        messages = await channel.history(limit=100000).flatten()
        for i in messages:
            truthfile.write(i.content + "\n")
        truthfile.close()
        await ctx.send("Done")
        #remove empty lines
        with open("databases/truth.txt", "r") as f:
            lines = f.readlines()
        with open("databases/truth.txt", "w") as f:
            for line in lines:
                if line.strip("\n"):
                    f.write(line)
        await ctx.send("Done")
        

    @commands.command()
    @commands.is_owner()
    async def makedarefile(self, ctx):
        #wipe file
        open("databases/dare.txt", "w").close()
        darefile = open("databases/dare.txt", "w")
        channel = self.client.get_channel(1031279167360212993)
        messages = await channel.history(limit=100000).flatten()
        for i in messages:
            darefile.write(i.content + "\n")
        darefile.close()
        await ctx.send("Done")
        #remove empty lines
        with open("databases/dare.txt", "r") as f:
            lines = f.readlines()
        with open("databases/dare.txt", "w") as f:
            for line in lines:
                if line.strip("\n"):
                    f.write(line)
        await ctx.send("Done")

    @commands.slash_command(name="truth", description="Get a truth",server_ids=betaservers)
    async def truth(self, ctx):
        if enabled_check(ctx) == True:
            truthbutton = Button(label="Truth", style=discord.ButtonStyle.green, custom_id="truth")
            darebutton = Button(label="Dare", style=discord.ButtonStyle.red, custom_id="dare")
            randombutton = Button(label="Random", style=discord.ButtonStyle.blurple, custom_id="random")
            linktoserver = Button(label="Join our server", style=discord.ButtonStyle.link, url="https://discord.gg/w4ZbjyVQEr")

            async def callback(interaction):
                if interaction.data["custom_id"] == "truth":
                    await interaction.response.send_message(embed=get_truth(), view=view)
                elif interaction.data["custom_id"] == "dare":
                    await interaction.response.send_message(embed=get_dare(), view=view)
                elif interaction.data["custom_id"] == "random":
                    await interaction.response.send_message(embed=get_random_truthordare(), view=view)
                
            truthbutton.callback = callback
            darebutton.callback = callback
            randombutton.callback = callback


            view = View(timeout=300)
            view.add_item(truthbutton)
            view.add_item(darebutton)
            view.add_item(randombutton)
            if random.randint(0, 10) == 10:
                view.add_item(linktoserver)

            await ctx.respond(embed=get_truth(), view=view)
        else:
            await ctx.respond("Truth or dare is disabled on this server")
        

    @commands.slash_command(name="dare", description="Get a dare",server_ids=betaservers)
    async def dare(self, ctx):
        if enabled_check(ctx) == True:
            truthbutton = Button(label="Truth", style=discord.ButtonStyle.green, custom_id="truth")
            darebutton = Button(label="Dare", style=discord.ButtonStyle.red, custom_id="dare")
            randombutton = Button(label="Random", style=discord.ButtonStyle.blurple, custom_id="random")
            linktoserver = Button(label="Join our server", style=discord.ButtonStyle.link, url="https://discord.gg/w4ZbjyVQEr")

            async def callback(interaction):
                if interaction.data["custom_id"] == "truth":
                    await interaction.response.send_message(embed=get_truth(), view=view)
                elif interaction.data["custom_id"] == "dare":
                    await interaction.response.send_message(embed=get_dare(), view=view)
                elif interaction.data["custom_id"] == "random":
                    await interaction.response.send_message(embed=get_random_truthordare(), view=view)
                
            truthbutton.callback = callback
            darebutton.callback = callback
            randombutton.callback = callback


            view = View(timeout=300)
            view.add_item(truthbutton)
            view.add_item(darebutton)
            view.add_item(randombutton)
            if random.randint(0, 10) == 10:
                view.add_item(linktoserver)

            await ctx.respond(embed=get_dare(), view=view)
        else:
            await ctx.respond("Truth or dare is disabled on this server")

    @commands.slash_command(name="truthordare", description="Get a truth or a dare",server_ids=betaservers,pass_context=True)
    async def truthordare(self, ctx):
        if enabled_check(ctx) == True:
            truthbutton = Button(label="Truth", style=discord.ButtonStyle.green, custom_id="truth")
            darebutton = Button(label="Dare", style=discord.ButtonStyle.red, custom_id="dare")
            randombutton = Button(label="Random", style=discord.ButtonStyle.blurple, custom_id="random")
            linktoserver = Button(label="Join our server", style=discord.ButtonStyle.link, url="https://discord.gg/w4ZbjyVQEr")

            async def callback(interaction):
                if interaction.data["custom_id"] == "truth":
                    await interaction.response.send_message(embed=get_truth(), view=view)
                elif interaction.data["custom_id"] == "dare":
                    await interaction.response.send_message(embed=get_dare(), view=view)
                elif interaction.data["custom_id"] == "random":
                    await interaction.response.send_message(embed=get_random_truthordare(), view=view)
                
            truthbutton.callback = callback
            darebutton.callback = callback
            randombutton.callback = callback


            view = View(timeout=300)
            view.add_item(truthbutton)
            view.add_item(darebutton)
            view.add_item(randombutton)
            if random.randint(0, 10) == 10:
                view.add_item(linktoserver)

            await ctx.respond(embed=get_random_truthordare(), view=view)
            
            

        else:
            await ctx.respond("Truth or dare is disabled on this server")

            


def setup(client):
    client.add_cog(TruthOrDare(client))
