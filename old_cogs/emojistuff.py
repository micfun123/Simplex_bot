import datetime
import discord
from discord.ext import commands
from tools import log


class emoji(commands.Cog):
    """All emoji stuff"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["emofy"], name="emojify", description="Converts text to emojis"
    )
    async def emojify_(self, ctx, *, text: str):
        """
        Turns text into emojis
        """
        text = text.lower()
        emojis = []
        for char in text:
            if char.isdecimal():
                num_to_emoji = {
                    "0": "zero",
                    "1": "one",
                    "2": "two",
                    "3": "three",
                    "4": "four",
                    "5": "five",
                    "6": "six",
                    "7": "seven",
                    "8": "eight",
                    "9": "nine",
                }
                emojis.append(f":{num_to_emoji.get(char)}:")

            elif char.isalpha():
                emojis.append(f":regional_indicator_{char}:")

            elif char in "?!#+-":
                special_char_to_emoji = {
                    "?": "question",
                    "!": "exclamation",
                    "#": "hash",
                    "+": "heavy_plus_sign",
                    "-": "heavy_minus_sign",
                }
                emojis.append(f":{special_char_to_emoji.get(char)}:")

            else:
                emojis.append(char)

        await ctx.send("".join(emojis))


def setup(bot):
    bot.add_cog(emoji(bot))
