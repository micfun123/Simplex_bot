import discord
from discord.commands.core import SlashCommand
from discord.ext import commands
from translate import Translator

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "translate",help="Translate text from one language to another. You must use the language code, not the language name. EG Arabic = ar")
    async def translate_(self, ctx, lang, *, text):
        translator = Translator(to_lang=lang)
        translation = translator.translate(text)
        embed = discord.Embed(title=f'Translation', description=translation, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name = "bin", help="number to Binary")
    async def bin_(self, ctx, *, text):
        embed = discord.Embed(title=f'Binary', description=bin(int(text)), color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="hex",help="number to Hex")
    async def hex_(self, ctx, *, text):
        embed = discord.Embed(title=f'Hex', description=hex(int(text)), color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name = "oct",help="number to Octal")
    async def oct_(self, ctx, *, text):
        embed = discord.Embed(title=f'Octal', description=oct(int(text)), color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name = "dec",help="number to Decimal")
    async def dec_(self, ctx, *, text):
        embed = discord.Embed(title=f'Decimal', description=int(text), color=0x00ff00)
        await ctx.send(embed=embed)


    
    @discord.slash_command(name = "translate",description="Translate text from one language to another. You must use the language code EG Arabic = ar")
    async def translate(self, ctx, lang, *, text):
        translator = Translator(to_lang=lang)
        translation = translator.translate(text)
        embed = discord.Embed(title=f'Translation', description=translation, color=0x00ff00)
        await ctx.respond(embed=embed)

    @discord.slash_command(name = "bin",description="number to Binary")
    async def bin(self, ctx, *, text):
        embed = discord.Embed(title=f'Binary', description=bin(int(text)), color=0x00ff00)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="hex",description="number to Hex")
    async def hex(self, ctx, *, text):
        embed = discord.Embed(title=f'Hex', description=hex(int(text)), color=0x00ff00)
        await ctx.respond(embed=embed)

    @discord.slash_command(name = "oct",description="number to Octal")
    async def oct(self, ctx, *, text):
        embed = discord.Embed(title=f'Octal', description=oct(int(text)), color=0x00ff00)
        await ctx.respond(embed=embed)

    @discord.slash_command(name = "dec",description="number to Decimal")
    async def dec(self, ctx, *, text):
        embed = discord.Embed(title=f'Decimal', description=int(text), color=0x00ff00)
        await ctx.respond(embed=embed)


        
def setup(client):
    client.add_cog(Translate(client)) 
