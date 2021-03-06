# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

from datetime import datetime
import discord
from embed import *
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

    message.content = str.lower(message.content)

    # gives the command to play David's playlist
    if message.content.startswith('$$ david'):
        await message.channel.send('-p https://open.spotify.com/playlist/2pOCpGDfekUKDN6Mzr1NGi')

    if message.content.startswith('$$ mostgain'):
        await message.channel.send(mostGain())

    if message.content.startswith('$$ mostloss'):
        await message.channel.send(mostLoss())

    # TODO: fix/improve  how the symbol is parsed
    if message.content.startswith('$$ price '):
        symbol = message.content.split()[2]
        price = currentPrice(symbol)
        if price == None:
            await message.channel.send("symbol not found")
            return

        time = datetime.now()
        date = datetime.today().weekday()
        currTime = time
        closeTime = time.replace(hour=21, minute=0, second=0, microsecond=0)
        openTime = time.replace(hour=14, minute=30, second=0, microsecond=0)

        if currTime > openTime and currTime < closeTime and date != 6 and date != 5:
            marketStatus = " (current price)"
        else:
            marketStatus= " (price at close)"

        change = oneDayPriceChange(symbol)
        percentDiff = changePercent(symbol)

        msg = "{}: ${} {} \n {} (%{})".format(str.upper(symbol), price, marketStatus, change, percentDiff)
        await message.channel.send(msg)

    if message.content.startswith('$$ embed'):
        print(message)
        await message.channel.send(embed = embedMessage(message))

client.run(os.getenv('TOKEN'))
