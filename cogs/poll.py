import discord
from discord.ext import commands
import asyncio
from discord import Embed

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Polls(commands.Cog):
    """Poll voting system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='poll')
    @commands.guild_only()
    async def poll(self, ctx, *, question):
        """Interactively creates a poll with the following question.
        To vote, use reactions!
        """

        # a list of messages to delete when we're all done
        messages = [ctx.message]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        for i in range(20):
            messages.append(await ctx.send(f'Say poll option or {ctx.prefix}cancel to publish poll.'))

            try:
                entry = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f'{ctx.prefix}cancel'):
                break

            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass # oh well
        
        answer = '\n'.join(f'{keycap}: {content}' for keycap, content in answers)
        
        em = discord.Embed(title=question, description=answer,color=0x20BEFF)
        em.set_footer(text=f'Poll created by {ctx.author}')

        actual_poll = await ctx.send(embed=em)
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Missing the question.')

    @commands.command(name='quickpoll')
    @commands.guild_only()
    async def quickpoll__command(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass
        
        em = discord.Embed(title=question, description='\n'.join(f'{keycap}: {content}' for keycap, content in choices),color=0x20BEFF)
        em.set_footer(text=f'Poll created by {ctx.author}')

        poll = await ctx.send(embed=em)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

    @commands.slash_command(name='quickpoll', description='Makes a poll quickly.')
    async def quickpoll__slash(self, ctx, question: str, choise_1, choise_2, choise_3=None, choise_4=None, choise_5=None, choise_6=None, choise_7=None, choise_8=None, choise_9=None, choise_10=None, choise_11=None, choise_12=None, choise_13=None, choise_14=None, choise_15=None, choise_16=None, choise_17=None, choise_18=None, choise_19=None, choise_20=None):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len([choise_1, choise_2, choise_3, choise_4, choise_5, choise_6, choise_7, choise_8, choise_9, choise_10, choise_11, choise_12, choise_13, choise_14, choise_15, choise_16, choise_17, choise_18, choise_19, choise_20]) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len([choise_1, choise_2, choise_3, choise_4, choise_5, choise_6, choise_7, choise_8, choise_9, choise_10, choise_11, choise_12, choise_13, choise_14, choise_15, choise_16, choise_17, choise_18, choise_19, choise_20]) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        choses = [choise_1, choise_2, choise_3, choise_4, choise_5, choise_6, choise_7, choise_8, choise_9, choise_10, choise_11, choise_12, choise_13, choise_14, choise_15, choise_16, choise_17, choise_18, choise_19, choise_20]
        choices = [(to_emoji(e), v) for e, v in enumerate(choses) if v is not None]
        em = discord.Embed(title=question, description='\n'.join(f'{keycap}: {content}' for keycap, content in choices),color=0x20BEFF)
        em.set_footer(text=f'Poll created by {ctx.author}')

        poll = await ctx.send(embed=em)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)
        await ctx.respond("Poll Ceated!", ephemeral=True)

def setup(bot):
    bot.add_cog(Polls(bot))