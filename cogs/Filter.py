import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup # Correct import for this style
import aiohttp
import aiofiles
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

class Filter(commands.Cog):
    """
    Applies fun image filter and overlay effects to user profile pictures
    using a slash command group.
    """
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
        self.temp_storage_path = "./tempstorage"
        # Ensure the temporary storage directory exists
        if not os.path.exists(self.temp_storage_path):
            os.makedirs(self.temp_storage_path)

    def cog_unload(self):
        # Gracefully close the aiohttp session when the cog is unloaded.
        self.client.loop.create_task(self.session.close())

    # Create a slash command group in the style you provided
    filter = SlashCommandGroup("filter", "Applies an image filter to an avatar.")

    async def _create_image_and_send(self, ctx: discord.ApplicationContext, endpoint: str, member: discord.Member):
        """
        A generalized function to handle API requests, file creation, and sending.
        
        Args:
            ctx: The discord.ApplicationContext from the command.
            endpoint: The specific API endpoint for the desired filter.
            member: The Discord member whose avatar will be used.
        """
        # Acknowledge the command immediately to prevent timeout errors
        await ctx.defer()

        if member is None:
            member = ctx.author

        avatar_url = str(member.display_avatar.url)
        api_url = f"https://some-random-api.com/canvas/{endpoint}"
        params = {'avatar': avatar_url}
        temp_file_path = None # Define here to ensure it's in scope for finally block

        try:
            async with self.session.get(api_url, params=params) as resp:
                if resp.status != 200:
                    logging.error(f"API Error: '{endpoint}' returned status {resp.status}")
                    await ctx.followup.send(f"😥 The image API isn't working right now. Please try again later.", ephemeral=True)
                    return

                # Determine file extension from Content-Type header
                content_type = resp.headers.get('Content-Type', '')
                extension = 'gif' if 'gif' in content_type else 'png'
                temp_file_path = os.path.join(self.temp_storage_path, f"overlay_{ctx.author.id}_{endpoint}.{extension}")

                data = await resp.read()
                async with aiofiles.open(temp_file_path, mode="wb") as f:
                    await f.write(data)

            # Send the file as a followup to the deferred response
            await ctx.followup.send(file=discord.File(temp_file_path))

        except aiohttp.ClientError as e:
            logging.error(f"Network error during API call: {e}")
            await ctx.followup.send("A network error occurred while connecting to the image API.", ephemeral=True)
        except IOError as e:
            logging.error(f"File write error: {e}")
            await ctx.followup.send("An error occurred while saving the image file.", ephemeral=True)
        finally:
            # IMPORTANT: Ensure the temporary file is always deleted
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    # --- Grouped Slash Commands ---

    @filter.command(name="jail", description="Puts a jail overlay on an avatar.")
    async def jail(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "jail", member)

    @filter.command(name="wasted", description="Puts a 'wasted' (GTA) overlay on an avatar.")
    async def wasted(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "wasted", member)
        
    @filter.command(name="comrade", description="Puts a 'comrade' overlay on an avatar.")
    async def comrade(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "comrade", member)

    @filter.command(name="passed", description="Puts a 'passed' (GTA) overlay on an avatar.")
    async def passed(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "passed", member)

    @filter.command(name="triggered", description="Creates a 'triggered' GIF from an avatar.")
    async def triggered(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "triggered", member)

    @filter.command(name="greyscale", description="Applies a greyscale filter to an avatar.")
    async def greyscale(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "greyscale", member)

    @filter.command(name="sepia", description="Applies a sepia filter to an avatar.")
    async def sepia(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "sepia", member)

    @filter.command(name="pixelate", description="Pixelates an avatar.")
    async def pixelate(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "pixelate", member)
    
    @filter.command(name="blurple", description="Applies the new blurple filter to an avatar.")
    async def blurple(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "blurple2", member)

    @filter.command(name="blurpleold", description="Applies the old blurple filter to an avatar.")
    async def blurpleold(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        await self._create_image_and_send(ctx, "blurple", member)


def setup(bot):
    """The setup function to add the cog to the bot."""
    bot.add_cog(Filter(bot))