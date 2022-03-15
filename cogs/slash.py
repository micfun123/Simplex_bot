# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option, SlashCommand
import json
import random
import qrcode
import os

def mic(ctx):
    return ctx.author.id == 481377376475938826

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="invite", description="Creates 10 day invite for this server")
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.respond(link)

    @commands.slash_command(name="botinvite", description="Invite simplex to your server :)")
    async def botinvite(self, ctx):
        await ctx.respond(embed=discord.Embed(title="Invite **'Simplex'?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    
    @slash_command(name="suggest", description="Suggest something for Simplex")
    async def suggest(self, ctx, suggestion: Option(str, "The suggestion", required=True)):
        sid = await self.client.fetch_channel(908969607266730005)
        em = discord.Embed(
            title= "Suggestion:",
            description=f"By: {ctx.author.name}\n\n{suggestion}",
            color=discord.Color.random()
        )
        await sid.send(embed=em, content=ctx.author.id)
        await ctx.respond("Thank you for you suggestion!")

    @commands.slash_command(name="ping", description="shows you the bots ping")
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.client.latency * 1000)}ms")

    @commands.slash_command(name="rps", description="Plays rock paper scissors with the bot")
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.respond(embed=em)


    
    @slash_command(name="reload", description="reloads a cog")
    @commands.check(mic)
    async def reload(self, ctx, extension:Option(str, "Cog Name", required=True, choices=cogs)):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.respond(embed=embed)

    @slash_command()
    async def donations(self,ctx):
        em = discord.Embed(title = 'Donation', description = 'Donate to the bot to help keep it running!', color = 0x8BE002)
        em.add_field(name = ':BTC :', value = '**3Fi97A4fLw8Yycv7F3DwSfMgBJ3zjB1AFL**')
        em.add_field(name = ':ETH :', value = '**0x7Cfa740738ab601DCa9740024ED8DB585E2ed7478**')
        em.add_field(name = ':Doge :', value = '**DQVkWKqGoTGUY9MeN3HiUt49JfcC9aE7fp**')
        em.add_field(name = ':MPL  :', value = '**0xbDBb6403CA6D1681F0ef7A2603aD65a9F09AF138**')
        em.add_field(name = ':XMR  :', value = '**43rsynRD1qtCA1po9myFsc7ti5havFcXUZPdSZuMexU4DnEyno55TE16eWqFkMLMbwZ7DuRW4ow5kcWzQQYu96NH7XMk6cE**')
        
        await ctx.respond(embed = em)
 
    @slash_command(name="emojify", description="Converts text to emojis")
    async def emojify(self, ctx, *, text: str):
        """
        Turns text into emojis
        """
        text = text.lower()
        emojis = []
        for char in text:
            if char.isdecimal():
                num_to_emoji = {
                    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
                    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
                }
                emojis.append(f":{num_to_emoji.get(char)}:")

            elif char.isalpha():
                emojis.append(f":regional_indicator_{char}:")
    
            elif char in "?!#+-":
                special_char_to_emoji = {
                    "?": "question", "!": "exclamation", "#": "hash",
                    "+": "heavy_plus_sign", "-": "heavy_minus_sign"
                }
                emojis.append(f":{special_char_to_emoji.get(char)}:")
            
            else:
                emojis.append(char)

        await ctx.respond("".join(emojis))

    @slash_command(name="qrcode", description = "Generate a QR code")
    async def qrcode_slash(self, ctx, *, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('qrcode.png')
        await ctx.respond(file=discord.File('qrcode.png'))

    @slash_command(name="avatar")
    async def avatar(self, ctx, *, member):
        
        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.respond(embed=message)

def setup(client):
    client.add_cog(Slash(client))