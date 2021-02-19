# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

import discord
import os
from stockInfo import *
from datetime import datetime


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

    # TODO: fix/improve  how the symbol is parsed
    if message.content.startswith('$$ price '):
        price = currentPrice(message.content[9:])
        ret = str.upper(message.content[9:]) + ": $" + str(price)

        time = datetime.now()
        currTime = time
        closeTime = time.replace(hour = 16, minute = 0, second = 0, microsecond = 0)
        openTime = time.replace(hour = 9, minute = 30, second = 0, microsecond = 0)

        if currTime > closeTime or currTime < openTime:
            ret += " (price at close)"
        else:
            ret += " (current price)"
        await message.channel.send(ret)


client.run(os.getenv('TOKEN'))
