# nextcord
import nextcord
import nextcord.utils
from nextcord import voice_client
from nextcord.ext import commands

# builtin modules
import random
from os import path, listdir
from asyncio import sleep

# Agnes library imports
import config

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.loop_is_running = False

    async def play_sound_effect(self, ctx):
        try:
            if self.vc:
                sound_dir = r'D:\Users\Tanner\Music\agnes_sounds'
                choose = random.choice(listdir(r'D:\Users\Tanner\Music\agnes_sounds'))
                sound = path.join(sound_dir, choose)
                self.vc.play(nextcord.FFmpegPCMAudio(executable=r'C:\Program Files (x86)\ffmpeg-4.3.1-win64-static\bin\ffmpeg.exe', source=sound))
                self.vc.source = nextcord.PCMVolumeTransformer(self.vc.source, volume=0.3)
            else:
                await ctx.send('Please connect me to a voice channel first.')
        except Exception as e:
            # is raised if someone spams playsound and audio is already playing.
            print(e)
            return

    @commands.command(name='voiceconnect', hidden=True, aliases=['connectvoice', 'joinvoice', 'voicejoin'])
    @commands.check(lambda ctx: ctx.author.id in config.ADMIN_IDS)
    async def __voiceconnect(self, ctx, *, voice_channel=None):
        """For testing purposes. Connects Agnes to a voice channel. If no parameters
        are given, she connects to the voice channel the invoker is in.
        """
        if self.vc:
            # disconnects if already in a voice channel:
            await ctx.voice_client.disconnect()
            self.vc = None
        if voice_channel is None:
            try:
                connection = ctx.author.voice.channel
            except AttributeError:
                connection = None
        else:
            connection = nextcord.utils.get(ctx.guild.channels, name=voice_channel)
            if not connection:
                await ctx.send(f'I couldn\'t find a channel called "{voice_channel}".')
                return
        if connection:
            vc = await connection.connect()
            self.vc = vc
            print(f'Connected to voice channel {connection.name}.')
        else:
            await ctx.send('It looks like you\'re not in a voice channel. Please connect and try again.')

    @commands.command(name='voiceleave', hidden=True, aliases=['voicedisconnect', 'leavevoice'])
    async def __voiceleave(self, ctx):
        """For testing purposes. Disconnects Agnes from voice."""
        if self.vc:
            await ctx.voice_client.disconnect()
            self.vc = None
        else:
            return

    @commands.command(name='playsound', hidden=True)
    @commands.check(lambda ctx: ctx.author.id in config.ADMIN_IDS)
    async def __playsound(self, ctx):
        """For testing purposes. Plays a sound effect if Agnes is in a voice channel."""
        await self.play_sound_effect(ctx)

    @commands.command(name='stop', hidden=True)
    async def __stop(self, ctx):
        """Stops playback."""
        if self.vc:
            if self.vc.is_playing():
                await self.vc.stop()
        else:
            return


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """TODO"""
        return
        if before.channel is None and after.channel is not None:
            print(f'{member.name} joined {after.channel.name}')
            member_count = len(after.channel.members)
            print(f'member count = {member_count}')
            if member_count == 1:
                print(f'connecting to {after.channel.name} to scare {member.name}')
                vc = await after.channel.connect()
                self.vc = vc
                try:
                    if self.vc:
                        sound_dir = r'D:\Users\Tanner\Music\agnes_sounds'
                        choose = random.choice(listdir(r'D:\Users\Tanner\Music\agnes_sounds'))
                        sound = path.join(sound_dir, choose)
                        self.vc.play(discord.FFmpegPCMAudio(executable=r'C:\Program Files (x86)\ffmpeg-4.3.1-win64-static\bin\ffmpeg.exe', source=sound))
                        self.vc.source = discord.PCMVolumeTransformer(self.vc.source, volume=0.3)
                        while self.vc.is_playing():
                            await sleep(1)
                        await after.channel.guild.voice_client.disconnect()
                    else:
                        await after.send('Please connect me to a voice channel first.')
                        return
                except Exception as e:
                    # is raised if someone spams playsound and audio is already playing.
                    print(e)
                    return
            await after.channel.guild.voice_client.disconnect()

    @commands.command()
    @commands.check(lambda ctx: ctx.author.id in config.ADMIN_IDS)
    async def soundloop(self, ctx, *, interval='10'):
        """Initiates a loop that plays a sound every 5 - 10 minutes."""
        self.loop_is_running = True
        interval = int(interval)
        interval_mins = interval * 60
        print(f'Starting sound effect loop with interval {interval} mins.')
        while self.loop_is_running:
            await self.play_sound_effect(ctx)
            await sleep(interval_mins)

    @commands.command()
    async def endloop(self, ctx):
        """Ends the sound effect loop."""
        self.loop_is_running = False
        print('Sound effect loop ended.')
