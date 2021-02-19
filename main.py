# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

import discord
import os
from stockInfo import *

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # do not read messages from itself
    if message.author == client.user or not message.content.startswith('$$'):
        return

    # gives the command to play David's playlist
    if message.content.startswith('$$ David'):
        await message.channel.send(
            '-p https://open.spotify.com/playlist/2pOCpGDfekUKDN6Mzr1NGi')

    if message.content.startswith('$$ mostgain'):
        await message.channel.send(mostGain())

    if message.content.startswith('$$ mostloss'):
        await message.channel.send(mostLoss())

    if message.content.startswith('$$ price '):
        await message.channel.send(currentPrice(message.content[9:]))


client.run(os.getenv('TOKEN'))
