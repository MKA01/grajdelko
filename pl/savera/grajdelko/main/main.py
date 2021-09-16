import discord
from discord.ext import commands
from pl.savera.grajdelko.player.Player import Player

# discord declarations
client = discord.Client()
bot = commands.Bot(command_prefix='-')

# variables
player = Player(discord, client)

# queue loop
client.loop.create_task(player.player_queue_task())


# commands
@bot.command(name='join', help='Nakazuje botu dołączenie do kanału głosowego')
async def join(ctx):
    if await cock_block(ctx):
        return

    if not ctx.message.author.voice:
        await ctx.send('{0} nie jest połączony do żadnego kanału'.format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.channel.send('Dołączam do kanału {0}'.format(channel))
        await channel.connect()


@bot.command(name='leave', help='Nakazuje botu odłączenie się od kanału głosowego')
async def leave(ctx):
    if await cock_block(ctx):
        return

    voice_client = ctx.message.guild.voice_client

    if voice_client.is_connected():
        await ctx.send('Opuszczam kanał')
        await voice_client.disconnect()
    else:
        await ctx.send('Nie jestem połączony do żadnego kanału')
        return


@bot.command(name='play', help='Odtwarzanie muzyki spod wskazanego URL')
async def play(ctx, url):
    if await cock_block(ctx):
        return

    voice_client = ctx.message.guild.voice_client

    if ctx.message.author.voice and not voice_client:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice_client = ctx.message.guild.voice_client

    # if voice_client.is_playing():
    await player.queue.put({
        'ctx': ctx,
        'url': url,
        'voice_client': voice_client
    })

    await ctx.send('Piosenka dodana do kolejki.')
    # else:
    #     await player.play_song(ctx, url, voice_client)


@bot.command(name='pause', help='Pauzuje aktualną piosenkę')
async def pause(ctx):
    if await cock_block(ctx):
        return

    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send(':pause_button: Zapauzowano piosenkę :pause_button:')
    else:
        await ctx.send("Żadna piosenka nie jest odtwarzana.")


@bot.command(name='resume', help='Wznawia aktualną piosenkę')
async def resume(ctx):
    if await cock_block(ctx):
        return

    voice_client = ctx.message.guild.voice_client

    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send(':play_pause: Wznowiono piosenkę :play_pause:')
    else:
        await ctx.send("Żadna piosenka nie jest odtwarzana.")


@bot.command(name='stop', help='Zatrzymuje piosenkę')
async def stop(ctx):
    if await cock_block(ctx):
        return

    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Zatrzymano piosenkę')
    else:
        await ctx.send("Żadna piosenka nie jest odtwarzana.")


# events
@bot.event
async def on_ready():
    print('Zalogowano jako {0.user}'.format(bot))


# custom methods
async def cock_block(ctx):
    if ctx.message.author.id == 243344283862695936:
        return False
    else:
        await ctx.send('W dupach mamy <@{0}>. Nami... rządzi Papież.'.format(ctx.message.author.id))
        return True


# run with token
if __name__ == '__main__':
    bot.run('ODg3NzQ5ODg3NDczNjE4OTc1.YUIrgg.bqsG1QUdb4X-bE3Dg5RwhLvjSjI')
