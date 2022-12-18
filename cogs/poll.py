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

    @commands.slash_command(name='poll', description='Makes a poll quickly.')
    async def quickpoll__slash(self, ctx, question: str, choice_1, choice_2, choice_3=None, choice_4=None, choice_5=None, choice_6=None, choice_7=None, choice_8=None, choice_9=None, choice_10=None, choice_11=None, choice_12=None, choice_13=None, choice_14=None, choice_15=None, choice_16=None, choice_17=None, choice_18=None, choice_19=None, choice_20=None):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len([choice_1, choice_2, choice_3, choice_4, choice_5, choice_6, choice_7, choice_8, choice_9, choice_10, choice_11, choice_12, choice_13, choice_14, choice_15, choice_16, choice_17, choice_18, choice_19, choice_20]) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len([choice_1, choice_2, choice_3, choice_4, choice_5, choice_6, choice_7, choice_8, choice_9, choice_10, choice_11, choice_12, choice_13, choice_14, choice_15, choice_16, choice_17, choice_18, choice_19, choice_20]) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        choses = [choice_1, choice_2, choice_3, choice_4, choice_5, choice_6, choice_7, choice_8, choice_9, choice_10, choice_11, choice_12, choice_13, choice_14, choice_15, choice_16, choice_17, choice_18, choice_19, choice_20]
        choices = [(to_emoji(e), v) for e, v in enumerate(choses) if v is not None]
        em = discord.Embed(title=question, description='\n'.join(f'{keycap}: {content}' for keycap, content in choices),color=0x20BEFF)
        em.set_footer(text=f'Poll created by {ctx.author}')

        poll = await ctx.send(embed=em)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)
        await ctx.respond("Poll Ceated!", ephemeral=True)

def setup(bot):
    bot.add_cog(Polls(bot))