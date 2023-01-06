import discord
from discord.ext import commands
import asyncio
from discord import Embed
import sqlite3
import aiosqlite

rules = """
A set of rules - No going twice 
You must go in the order of the alphabet 
You cannot repeat a word
Start with A, example Apple / Bear / cottage cheese 
Keep repeating this order until you get to Z then start over again 
If you repeat you will lose the ability to keep playing.
A staff member may reset the game
"""

class letter_game(commands.Cog):
    """The Word games"""

   
    @commands.command()
    async def make_letter_game_db(self, ctx):
        con = sqlite3.connect("./databases/letter_game.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE server_letter_game (guild_id INTEGER, game_channel INTEGER, lastplayer INTEGER,longestgame INTEGER, currentlength INTEGER, attemps INTEGER, fails INTEGER")
        con.commit()
        await ctx.send("Done")

    @commands.command(name="how_to_letter_game")
    async def letter_game_rules(self,ctx):
        await ctx.send(rules)

    
def setup(bot):
    bot.add_cog(letter_game(bot))