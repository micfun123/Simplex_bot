import discord
from discord.ext import commands
from translate import Translator

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Translate text from one language to another. You must use the language code, not the language name. EG Arabic = ar")
    async def translate(self, ctx, lang, *, text):
        translator = Translator(to_lang=lang)
        translation = translator.translate(text)
        embed = discord.Embed(title=f'Translation', description=translation, color=0x00ff00)
        await ctx.send(embed=embed)

        
def setup(client):
    client.add_cog(Translate(client)) 
