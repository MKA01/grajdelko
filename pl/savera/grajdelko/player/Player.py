import asyncio
import datetime
from queue import PriorityQueue

import validators
import youtube_dl


class Player:
    queue = asyncio.Queue()
    # queue = PriorityQueue()
    play_next_song = asyncio.Event()
    next_song = None
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

    async def add_song_to_queue(self, ctx, url, voice_client):
        is_valid_url = validators.url(url)

        if is_valid_url:
            info = self.ytdl.extract_info(url, download=False)
        else:
            info = self.ytdl.extract_info('ytsearch:{0}'.format(url), download=False)['entries'][0]

        audio = self.discord.FFmpegPCMAudio(info['url'], **self.ffmpeg_options)

        if self.queue.empty():
            self.next_song = info['title']

        await self.queue.put({
            'audio': audio,
            'info': info,
            'ctx': ctx,
            'voice_client': voice_client
        })

        return info

    async def player_queue_task(self):
        while True:
            self.play_next_song.clear()
            current = await self.queue.get()

            if self.queue.empty():
                self.next_song = None

            await self.play_song(current['ctx'], current['info'], current['voice_client'], current['audio'])
            await self.play_next_song.wait()

    async def play_song(self, ctx, info, voice_client, audio):
        async with ctx.typing():
            embed = self.discord.Embed(title=':notes: Teraz leci ta piosenka :notes:',
                                       colour=self.discord.Color.green(),
                                       description='```css\n{0}\n```'.format(info['title']),
                                       url=info['webpage_url'])
            embed.set_image(url=info['thumbnail'])
            embed.add_field(name='Czas trwania:', value=datetime.timedelta(seconds=info['duration']), inline=True)
            embed.add_field(name='Dodał:', value='<@{0}>'.format(ctx.message.author.id), inline=True)
            embed.add_field(name='Następne w kolejce:', value=self.get_next_song())

            await ctx.send(embed=embed)

            voice_client.play(audio, after=self.toggle_next)

    def get_next_song(self):
        if not self.next_song:
            return 'Kolejka jest pusta'
        else:
            return self.next_song

    def toggle_next(self, idk_why_i_need_this):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)
