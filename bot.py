import discord
import asyncio
import pytube
from discord.ext import commands
from discord import FFmpegPCMAudio
from pytube import YouTube


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)


@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f'yendo a darle el corte a : {channel}')


@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send('Desconectado del canal de voz')
    else:
        await ctx.send('tengo que estar en el voice primero aweonao')
@bot.command()
async def play(ctx, url):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send('¡Tengo que estar en el canal de voz primero!')
        return

    try:
        if 'playlist' in url.lower():
            playlist = YouTube(url)
            await ctx.send(f'Reproduciendo la lista de reproducción: {playlist.title}')

            for video in playlist.videos:
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_source = discord.FFmpegPCMAudio(
                    audio_stream.url,
                    before_options="-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2"
                )
                voice_client.play(audio_source)

                while voice_client.is_playing():
                    await asyncio.sleep(1)

            await ctx.send('¡Terminó la lista de reproducción!')
        else:
            video = YouTube(url)
            best_audio = video.streams.get_audio_only()

            audio_source = discord.FFmpegPCMAudio(
                best_audio.url,
                before_options="-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2"
            )

            voice_client.play(audio_source)
            await ctx.send('dandole el corte con musica de yutube')

            while voice_client.is_playing():
                await asyncio.sleep(1)

            await ctx.send('termino la wea me tengo que ir a chupar zorra')

    except Exception as e:
        await ctx.send(f'Error: {str(e)}')



TOKEN = 'xxx'
bot.run(TOKEN)
