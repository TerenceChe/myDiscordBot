# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
import os
from database import *
import datetime
import discord
from embed import *
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
        await message.channel.send(most_gain())

    if message.content.startswith('$$ mostloss'):
        await message.channel.send(most_loss())

    # TODO: fix/improve  how the symbol is parsed
    if message.content.startswith('$$ price '):
        symbol = message.content.split()[2]
        price = current_price(symbol)
        if price is None:
            await message.channel.send("symbol not found")
            return

        time = datetime.datetime.now()
        date = datetime.datetime.today().weekday()
        curr_time = time
        close_time = time.replace(hour=21, minute=0, second=0, microsecond=0)
        open_time = time.replace(hour=14, minute=30, second=0, microsecond=0)

        if open_time < curr_time < close_time and date != 6 and date != 5:
            marketStatus = " (current price)"
        else:
            marketStatus = " (price at close)"

        change = one_day_price_change(symbol)
        percentDiff = change_percent(symbol)

        msg = "{0}: ${1:.2f} {2} \n {3} (%{4})".format(str.upper(symbol), price, marketStatus, change, percentDiff)
        await message.channel.send(msg)

    if message.content.startswith('$$ buy'):
        msg = message.content.split()
        symbol = msg[2]
        amount = int(msg[3])
        price = current_price(symbol)
        if(add_stock(message.author.id, symbol, amount, price)):
            msg = "successfully purchased {} shares of {}".format(amount, str.upper(symbol))
        else:
            msg = "not enough money to purchase stock"
        await message.channel.send(msg)

    if message.content.startswith('$$ embed'):
        print(message)
        await message.channel.send(embed=embedMessage(message))

client.run(os.getenv('TOKEN'))
