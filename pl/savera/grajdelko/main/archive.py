import discord
import youtube_dl
from discord.ext import commands, tasks
import os

if __name__ == '__main__':

    youtube_dl.utils.bug_reports_message = lambda: ''

    # discord declarations
    client = discord.Client()


    # youtube audio download

    # commands
    @bot.command(name='join', help='Nakazuje botu dołączenie do kanału głosowego')
    async def join(context):
        if not context.message.author.voice:
            await context.send('{0} nie jest połączony do żadnego kanału'.format(context.message.author.name))
            return
        else:
            channel = context.message.author.voice.channel
            await context.channel.send('Dołączam do kanału {0}'.format(channel))
            await channel.connect()


    @bot.command(name='leave', help='Nakazuje botu odłączenie się od kanału głosowego')
    async def leave(context):
        voice_client = context.message.guild.voice_client

        if voice_client.is_connected():
            await context.send('Opuszczam kanał')
            await voice_client.disconnect()
        else:
            await context.send('Nie jestem połączony do żadnego kanału')
            return


    # events
    @client.event
    async def on_ready():
        print('Zalogowano jako {0.user}'.format(client.user))



    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == '-test':
            await message.channel.send('chuj :)')

        if message.content == '-join':
            await message.channel.send('Dołączam do kanału {0}'.format(message.author.voice.channel))
            await message.author.voice.channel.connect()

        if message.content == '-leave':
            await message.channel.send('Opuszczam kanał')
            await message.guild.voice_client.disconnect()

    # run with token
    client.run('ODg3NzQ5ODg3NDczNjE4OTc1.YUIrgg.bqsG1QUdb4X-bE3Dg5RwhLvjSjI')
