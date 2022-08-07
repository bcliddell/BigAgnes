"""
TODO: change absolute file paths in all py files to relative paths.
"""

# nextcord
import nextcord
import nextcord.utils
from nextcord import voice_client
from nextcord.ext import commands

# builtin modules
import random
import re

# Agnes library imports
from AgnesUtil import AgnesUtil
import config

class Agnes(commands.Bot):
    """The abstraction of Agnes herself, a Bot object."""
    def __init__(self):
        intents = nextcord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        super().__init__(command_prefix=['!', 'Agnes, '], intents=intents)
        print('hello world!')
        # utils contains auth and util functions used inside Bot commands
        self.utils = AgnesUtil()

    async def on_ready(self):
        """Is called every time Agnes finishes booting up"""
        print('Terminator is activated.\n')
        # changes Agne's status to "Playing God"
        await self.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name='God'))

    async def on_message(self, message):
        """This function is called every time a message is sent"""

        # this is necessary to make @bot.event functions and @bot.command() functs compatible
        await self.process_commands(message)

        x = random.randint(1, 250)
        spot_regex = re.compile(r'(https://open.spotify.com/track/)(.*)(\?)(.*)')

        # -----Bookkeeping ifs-----
        if message.author == self.user or message.author.bot:
            # prevents the bot from responding to itself or other bots
            return
        if x == 1:
            # a 5% chance of responding with the :thank: emoji
            emoji = '<:thank:592156422150684712>'
            await message.add_reaction(emoji)

        # -----Context responses-----
        if 'acquiesce' in message.content:
            # prints on trigger word 'acquiesce'
            await message.channel.send('A C Q U I E S C E')
        if message.content.lower() in config.SWEARS:
            # prints on trigger word from swears list. Does not work in a sentence.
            await message.channel.send('Please don\'t fucking swear.')
        if 'i love you' in message.content.lower():
            # prints on trigger phrase 'I love you'.
            x = random.randint(0, 10)
            if x == 1:
                await message.channel.send(f'I eat ass {message.author.mention}')
            elif x == 2:
                await message.channel.send(f'Oh, um, well, I think we should just be friends, {message.author.mention}.')
            else:
                await message.channel.send(f'I love you {message.author.mention}')
        if 'sentient' in message.content.lower():
            # prints on trigger word 'sentient'.
            sentient_response = random.choice(config.SENTIENT_RESPONSES)
            await message.channel.send(sentient_response)
        if 'hello there' in message.content.lower():
            # General Kenobi!
            await message.channel.send('General Kenobi!')

        # spotify playlist generator
        mo = spot_regex.search(message.content)
        if mo:
            uri = mo.group(2)
            self.utils.add_song(uri)
            await message.add_reaction('👍')

    async def on_command(self, ctx):
        # check if user has the Restricted role
        if not (isinstance(ctx.channel, nextcord.channel.DMChannel) or isinstance(ctx.channel, nextcord.channel.GroupChannel)):
            usr = ctx.guild.get_member(ctx.author.id)
            if nextcord.utils.get(usr.roles, name="Restricted"):
                raise commands.MissingPermissions(["user does not have 'restricted' role."])

    async def on_command_error(self, ctx, error):
        """Overrides default commands.Bot command error handling."""
        if hasattr(ctx.command, 'on_error'):
            # prevents any commands with local on_command_error listeners from
            # being handled here.
            return
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'You tryna be sly {ctx.author.mention}? That command doesn\'t exist.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Hey there, looks like you forgot a required argument: `{error.param.name}`. Type `!help {ctx.command.name}` for more info.")
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"Sorry, I couldn't parse your argument for `{error.param.name}. Please check what you wrote and try again.")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"Sorry, your supreme leader, in their infinite wisdom, has disabled that command.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Sorry, you don't have permission to invoke that command. Get fuked.")
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"Sorry, you don't have permission to invoke that command. Get fuked.")
        else:
            # else raise error normally
            raise error
