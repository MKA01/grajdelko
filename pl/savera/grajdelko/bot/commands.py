import datetime
from pprint import pprint


def add_commands(bot, player, discord):
    @bot.command(name='join', help='Nakazuje botu dołączenie do kanału głosowego')
    async def join(ctx, *channel_name_args):
        if await cock_block(ctx):
            return

        channel_name = None

        if len(channel_name_args) == 1:
            channel_name = channel_name_args[0]
        elif len(channel_name_args) > 1:
            channel_name = ' '.join(channel_name_args)

        voice_channels = ctx.message.guild.voice_channels
        voice_channel = None

        for vc in voice_channels:
            if vc.name == channel_name:
                voice_channel = vc
                break

        if not ctx.message.author.voice:
            await ctx.send('{0} nie jest połączony do żadnego kanału'.format(ctx.message.author.name))
            return
        else:
            voice_client = ctx.message.guild.voice_client

            if voice_client and voice_client.is_connected():
                await voice_client.disconnect()

            if voice_channel:
                channel = voice_channel
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
    async def play(ctx, *args):
        if await cock_block(ctx):
            return

        url = None

        if len(args) < 1:
            await ctx.send('Nie wskazano żadnej piosenki.')
            return
        elif len(args) == 1:
            url = args[0]
        elif len(args) > 1:
            url = ' '.join(args)

        voice_client = ctx.message.guild.voice_client

        if ctx.message.author.voice and not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            voice_client = ctx.message.guild.voice_client

        info = await player.add_song_to_queue(ctx, url, voice_client)
        discord = player.discord

        embed = discord.Embed(title=info['title'], colour=discord.Colour(0x1), url=info['webpage_url'])
        embed.set_thumbnail(url=info['thumbnail'])
        embed.set_author(name="Piosenka dodana do kolejki", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="Kanał", value=info['uploader'], inline=True)
        embed.add_field(name="Czas trwania", value=datetime.timedelta(seconds=info['duration']), inline=True)

        await ctx.send(content=":musical_note: Wyszukuję :mag_right: {0}".format(url), embed=embed)

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

    @bot.command(name='skip', help='Pomija piosenkę')
    async def skip(ctx):
        if await cock_block(ctx):
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send(":fast_forward: Pominięto piosenkę :rage:")
            player.toggle_next(None)
        else:
            await ctx.send("Żadna piosenka nie jest odtwarzana.")
            return


async def cock_block(ctx):
    if ctx.message.author.id == 243344283862695936:
        return False
    else:
        await ctx.send('W dupach mamy <@{0}>. Nami... rządzi Papież.'.format(ctx.message.author.id))
        return True
