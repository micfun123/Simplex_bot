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

    @commands.command(name="reload", help="♻️ Reload a specific cog or all cogs.")
    @commands.check(is_owner)
    async def reload(self, ctx, cog: str = None):
        await ctx.send("♻️ Reloading cogs...")

        path = "./cogs"
        failed = []

        if cog:
            cogs_to_reload = [f"cogs.{cog}"]
        else:
            cogs_to_reload = [f"cogs.{f[:-3]}" for f in os.listdir(path) if f.endswith(".py")]

        for cog_path in cogs_to_reload:
            try:
                await self.bot.reload_extension(cog_path)
            except Exception as e:
                failed.append((cog_path, str(e)))

        if not failed:
            await ctx.send("✅ All cogs reloaded successfully!")
        else:
            msg = "\n".join(f"❌ `{name}`: {err}" for name, err in failed)
            await ctx.send(f"Some cogs failed to reload:\n```{msg}```")

    @commands.command(name="diff", help="📝 Show local code changes (git diff).")
    @commands.check(is_owner)
    async def diff(self, ctx):
        try:
            result = subprocess.run(["git", "diff", "--shortstat"], capture_output=True, text=True)
            diff = result.stdout.strip() or "No changes detected."
            await ctx.send(f"📄 Git Diff:\n```{diff}```")
        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")

async def setup(bot):
    await bot.add_cog(GitManager(bot))
