from discord.ext import commands
import asyncio


class utilities(commands.Cog):
    def __init__(self, client): 
        self.client = client 
    

    @commands.command(aliases=['sug'])
    async def suggest(self, ctx, *, suggestion):
        sid = await self.client.fetch_channel(908969607266730005)
        await sid.send(f"Suggestion:\n{suggestion}\n\nBy: {ctx.author.name}\nID: {ctx.author.id}")
        await ctx.send("Thank you for you suggestion!")


def setup(bot):
    bot.add_cog(utilities(bot))