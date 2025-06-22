import discord
from discord.ext import commands
import subprocess
import os
import asyncio

OWNER_ID = 481377376475938826

class GitManager(commands.Cog):
    """⚙️ Git and Cog management tools for the bot owner."""

    def __init__(self, bot):
        self.bot = bot

    def is_owner(ctx):
        return ctx.author.id == OWNER_ID

    @commands.command(name="pull", help="📥 Pull the latest code from git.")
    @commands.check(is_owner)
    async def pull(self, ctx):
        await ctx.send("🔄 Pulling from Git...")

        try:
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            output = result.stdout or result.stderr
            await ctx.send(f"```{output}```")
        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")

    @commands.command(name="reload", help="♻️ Reload a specific cog.")
    @commands.check(is_owner)
    async def reload(self, ctx, cog: str):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully reloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to reload `cogs.{cog}`:\n```{e}```")

    @commands.command(name="load", help="📦 Load a cog.")
    @commands.check(is_owner)
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully loaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to load `cogs.{cog}`:\n```{e}```")

    @commands.command(name="unload", help="📤 Unload a cog.")
    @commands.check(is_owner)
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully unloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to unload `cogs.{cog}`:\n```{e}```")

    @commands.command(name="diff", help="📝 Show local code changes (git diff).")
    @commands.check(is_owner)
    async def diff(self, ctx):
        try:
            result = subprocess.run(["git", "diff", "--shortstat"], capture_output=True, text=True)
            diff = result.stdout.strip() or "No changes detected."
            await ctx.send(f"📄 Git Diff:\n```{diff}```")
        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")

def setup(bot):
    bot.add_cog(GitManager(bot))
