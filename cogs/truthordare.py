import random
import aiosqlite
import discord
import os
import asyncio
from discord.ext import commands
from discord.ui import Button, View

class TruthOrDareView(View):
    """Persistent view for Truth or Dare buttons."""
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.green, custom_id="persistent:truth")
    async def truth_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.cog.is_enabled(interaction.guild_id):
            return await interaction.response.send_message("Truth or dare is disabled on this server.", ephemeral=True)
        embed = await self.cog.get_truth_embed(interaction)
        await interaction.response.send_message(embed=embed, view=self)

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.red, custom_id="persistent:dare")
    async def dare_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.cog.is_enabled(interaction.guild_id):
            return await interaction.response.send_message("Truth or dare is disabled on this server.", ephemeral=True)
        embed = await self.cog.get_dare_embed(interaction)
        await interaction.response.send_message(embed=embed, view=self)

    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple, custom_id="persistent:random")
    async def random_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.cog.is_enabled(interaction.guild_id):
            return await interaction.response.send_message("Truth or dare is disabled on this server.", ephemeral=True)
        if random.random() < 0.5:
            embed = await self.cog.get_truth_embed(interaction)
        else:
            embed = await self.cog.get_dare_embed(interaction)
        await interaction.response.send_message(embed=embed, view=self)

class TruthOrDare(commands.Cog):
    """🎲 Classic Truth or Dare with optimized performance and modern UI."""

    def __init__(self, bot):
        self.bot = bot
        self.db_path = "databases/truthordare.db"
        self.truth_file = "databases/truth.txt"
        self.dare_file = "databases/dare.txt"
        self._truths = []
        self._dares = []
        self._enabled_cache = {} # guild_id: bool
        self.bot.loop.create_task(self.load_questions())

    async def load_questions(self):
        """Loads truth and dare questions into memory for fast access."""
        try:
            if os.path.exists(self.truth_file):
                async with asyncio.Lock(): # Simple concurrency protection
                    with open(self.truth_file, "r") as f:
                        self._truths = [line.strip() for line in f.readlines() if line.strip()]
            
            if os.path.exists(self.dare_file):
                with open(self.dare_file, "r") as f:
                    self._dares = [line.strip() for line in f.readlines() if line.strip()]
            
            # Fallbacks if files are empty or missing
            if not self._truths: self._truths = ["Tell us a secret.", "Who is your crush?"]
            if not self._dares: self._dares = ["Do 10 pushups.", "Send a silly emoji."]
        except Exception as e:
            print(f"Error loading questions: {e}")

    async def is_enabled(self, guild_id: int) -> bool:
        """Check if Truth or Dare is enabled for a guild, with caching."""
        if guild_id in self._enabled_cache:
            return self._enabled_cache[guild_id]
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT toggel FROM truthordare WHERE server_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                enabled = bool(row[0]) if row else False
                self._enabled_cache[guild_id] = enabled
                return enabled

    async def get_truth_embed(self, interaction: discord.Interaction):
        text = random.choice(self._truths)
        return self._format_embed("Truth", text, interaction, discord.Color.green())

    async def get_dare_embed(self, interaction: discord.Interaction):
        text = random.choice(self._dares)
        return self._format_embed("Dare", text, interaction, discord.Color.red())

    def _format_embed(self, title, text, interaction, color):
        # Handle member replacement
        if "{{randomly_selected_userer}}" in text:
            # Filter out bots and the requester for more fun
            eligible_members = [m for m in interaction.guild.members if not m.bot and m.id != interaction.user.id]
            if not eligible_members: eligible_members = interaction.guild.members # Fallback
            target = random.choice(eligible_members)
            text = text.replace("{{randomly_selected_userer}}", target.display_name)
        
        embed = discord.Embed(title=title, description=text, color=color)
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        return embed

    @discord.slash_command(name="truth", description="Get a truth question")
    async def truth(self, ctx):
        if not await self.is_enabled(ctx.guild.id):
            return await ctx.respond("Truth or dare is disabled on this server.", ephemeral=True)
        await ctx.respond(embed=await self.get_truth_embed(ctx), view=TruthOrDareView(self))

    @discord.slash_command(name="dare", description="Get a dare challenge")
    async def dare(self, ctx):
        if not await self.is_enabled(ctx.guild.id):
            return await ctx.respond("Truth or dare is disabled on this server.", ephemeral=True)
        await ctx.respond(embed=await self.get_dare_embed(ctx), view=TruthOrDareView(self))

    @discord.slash_command(name="truthordare", description="Get a random truth or dare")
    async def truthordare(self, ctx):
        if not await self.is_enabled(ctx.guild.id):
            return await ctx.respond("Truth or dare is disabled on this server.", ephemeral=True)
        
        if random.random() < 0.5:
            embed = await self.get_truth_embed(ctx)
        else:
            embed = await self.get_dare_embed(ctx)
        await ctx.respond(embed=embed, view=TruthOrDareView(self))

    @discord.slash_command(name="toggle_truthordare", description="Enable or disable Truth or Dare")
    @commands.has_permissions(administrator=True)
    async def truthordare_toggle(self, ctx):
        async with aiosqlite.connect(self.db_path) as db:
            enabled = await self.is_enabled(ctx.guild.id)
            new_status = 0 if enabled else 1
            await db.execute("""
                INSERT INTO truthordare (server_id, toggel) VALUES (?, ?)
                ON CONFLICT(server_id) DO UPDATE SET toggel = EXCLUDED.toggel
            """, (ctx.guild.id, new_status))
            await db.commit()
            
        self._enabled_cache[ctx.guild.id] = bool(new_status)
        status_text = "enabled" if new_status else "disabled"
        await ctx.respond(f"✅ Truth or dare has been **{status_text}**!")
        
        # Optional promotion as in original
        if not new_status:
             await ctx.followup.send(
                "If you enjoy the bot, consider voting: https://top.gg/bot/902240397273743361",
                ephemeral=True
            )

    @commands.command(name="reload_questions", hidden=True)
    @commands.is_owner()
    async def reload_questions(self, ctx):
        """[Owner] Reload truth and dare questions from files."""
        await self.load_questions()
        await ctx.send(f"✅ Reloaded questions! (Truths: {len(self._truths)}, Dares: {len(self._dares)})")

    @commands.command(name="maketruthordarefile", hidden=True)
    @commands.is_owner()
    async def maketruthordarefile(self, ctx):
        """[Owner] Pulls messages from specific channels to populate truth and dare files."""
        await ctx.send("🔄 Generating files from channels...")
        
        try:
            # Truth channel
            truth_channel = self.bot.get_channel(1031279120623083560)
            if truth_channel:
                messages = await truth_channel.history(limit=None).flatten()
                with open(self.truth_file, "w") as f:
                    for msg in messages:
                        if msg.content:
                            f.write(msg.content.replace("\n", " ") + "\n")
            
            # Dare channel
            dare_channel = self.bot.get_channel(1031279167360212993)
            if dare_channel:
                messages = await dare_channel.history(limit=None).flatten()
                with open(self.dare_file, "w") as f:
                    for msg in messages:
                        if msg.content:
                            f.write(msg.content.replace("\n", " ") + "\n")
            
            await self.load_questions()
            await ctx.send(f"✅ Done! Loaded {len(self._truths)} truths and {len(self._dares)} dares.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
