import discord
from discord.ext import commands
from pl.savera.grajdelko.bot.commands import add_commands
from pl.savera.grajdelko.player.Player import Player

# discord declarations
client = discord.Client()
bot = commands.Bot(command_prefix='-')

# variables
player = Player(discord, client)

# queue loop
client.loop.create_task(player.player_queue_task())

# commands
add_commands(bot, player, discord)


# events
@bot.event
async def on_ready():
    print('Zalogowano jako {0.user}'.format(bot))


# run with token
if __name__ == '__main__':
    bot.run('TOKEN')
