import asyncio
import datetime
import os
import time
import traceback
import youtube_dl
import validators


class Player:
    queue = asyncio.Queue()
    play_next_song = asyncio.Event()
    youtube_dl.utils.bug_reports_message = lambda: ''
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': False,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'verbose': True,
        'skip_download': True
    }
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    def __init__(self, discord, client):
        self.discord = discord
        self.client = client

    async def play_song(self, ctx, url, voice_client):
        try:
            async with ctx.typing():
                is_valid_url = validators.url(url)

                if is_valid_url:
                    info = self.ytdl.extract_info(url, download=False)
                else:
                    info = self.ytdl.extract_info('ytsearch:{0}'.format(url), download=False)['entries'][0]

                embed = self.discord.Embed(title='Teraz gra', colour=self.discord.Color.green(),
                                           description='```css\n{0}\n```'.format(info['title']))
                embed.set_image(url=info['thumbnail'])
                embed.add_field(name='Czas trwania:', value=datetime.timedelta(seconds=info['duration']), inline=True)
                embed.add_field(name='Dodał:', value='<@{0}>'.format(ctx.message.author.id), inline=True)
                embed.add_field(name='Następne w kolejce:', value=self.get_next_song())

                await ctx.send(embed=embed)

                voice_client.play(self.discord.FFmpegPCMAudio(info['url'], **self.ffmpeg_options),
                                  after=self.toggle_next())
        except Exception:
            traceback.print_exc()
            await ctx.send(":scream: Wystąpił błąd podczas odtwarzania, proszę sprawdzić logi. :scream:")

    def get_next_song(self):
        return 'Kolejka jest pusta'

    async def player_queue_task(self):
        while True:
            self.play_next_song.clear()
            current = await self.queue.get()
            print('current from task {0}'.format(current))
            # current.start()
            voice_client = current['voice_client']
            while voice_client.is_playing():
                time.sleep(1)

            await self.play_song(current['ctx'], current['url'], voice_client)
            await self.play_next_song.wait()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)
