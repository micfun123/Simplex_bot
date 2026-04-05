import discord
from discord.ext import commands
import asyncio
import os

class GitManager(commands.Cog):
    """⚙️ Git and Cog management tools for the bot owner."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pull", help="📥 Pull the latest code from git.")
    @commands.is_owner()
    async def pull(self, ctx):
        """Pull the latest changes from the git repository."""
        await ctx.send("🔄 Pulling from Git...")

        try:
            process = await asyncio.create_subprocess_exec(
                "git", "pull",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            output = (stdout + stderr).decode()
            await ctx.send(f"```{output[:1900]}```")
        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")

    @commands.command(name="reload", help="♻️ Reload a specific cog.")
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully reloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to reload `cogs.{cog}`:\n```{e}```")

    @commands.command(name="load", help="📦 Load a cog.")
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully loaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to load `cogs.{cog}`:\n```{e}```")

    @commands.command(name="unload", help="📤 Unload a cog.")
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Successfully unloaded `cogs.{cog}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to unload `cogs.{cog}`:\n```{e}```")

    @commands.command(name="diff", help="📝 Show local code changes (git diff).")
    @commands.is_owner()
    async def diff(self, ctx):
        try:
            process = await asyncio.create_subprocess_exec(
                "git", "diff", "--shortstat",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            diff = stdout.decode().strip() or "No changes detected."
            await ctx.send(f"📄 Git Diff:\n```{diff}```")
        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")

def setup(bot):
    bot.add_cog(GitManager(bot))
