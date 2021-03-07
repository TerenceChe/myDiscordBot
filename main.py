# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

from database import *
import datetime
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

    # gives the command which plays David's playlist
    if message.content.startswith('$$ david'):
        await message.channel.send('-p https://open.spotify.com/playlist/2pOCpGDfekUKDN6Mzr1NGi')
        return

    # check which stock gained the most
    elif message.content.startswith('$$ mostgain') or message.content.startswith('$$ most gain'):
        await message.channel.send(most_gain())
        return

    # check which stock loss the most
    elif message.content.startswith('$$ mostloss') or message.content.startswith('$$ most loss'):
        await message.channel.send(most_loss())
        return

    # TODO: fix/improve how the symbol is parsed
    # check price of a particular stock
    elif message.content.startswith('$$ price '):
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
        return

    # buy shares of a stock
    elif message.content.startswith('$$ buy '):
        msg = message.content.split()
        symbol = msg[3]
        amount = int(msg[2])
        price = current_price(symbol)
        if add_stock(message.author.id, symbol, amount, price):
            msg = "successfully purchased {0} shares of {1} for a total of: ${2:.2f}".format(
                amount, str.upper(symbol), price * amount)

        else:
            msg = "not enough money to purchase stock"
        await message.channel.send(msg)
        return

    # sell shares of a stock
    elif message.content.startswith('$$ sell '):
        msg = message.content.split()
        symbol = msg[3]
        amount = int(msg[2])
        try:
            price = current_price(symbol)
        except IndexError:
            await message.channel.send("{0} is not a stock".format(str.upper(symbol)))
            return
        try:
            amount_sold = sell_stock(message.author.id, symbol, amount, price)
            await message.channel.send("successfully sold {0} shares of {1} for a total of: ${2:.2f}".format(
                    amount_sold, str.upper(symbol), amount * price))

        except NoStockError:
            await message.channel.send("you have no shares of {0}".format(str.upper(symbol)))
            return

    # check available balance
    elif message.content.startswith('$$ balance'):
        await message.channel.send("money available to trade: ${0:.2f}".format(user_balance(message.author.id)))
        return

    # check stats
    elif message.content.startswith('$$ checkstocks') or message.content.startswith('$$ check stocks'):
        user = message.author.id
        cursor = owned_stock_cursor(user)
        total = 0
        for n in cursor:
            stock = n.get('stock')
            amount = n.get('amount')
            price = current_price(stock)
            total += amount * price
            await message.channel.send("you have {0} shares of {1} which is worth: ${2:.2f}".format(
                amount, str.upper(stock), price * amount))

        await message.channel.send("total value in stocks: ${0:.2f}".format(total))
        balance = total + user_balance(user)
        await message.channel.send("total balance: ${0:.2f}".format(balance))
        return

    elif message.content.startswith('$$ embed'):
        print(message)
        await message.channel.send(embed=embedMessage(message))
        return

client.run(os.getenv('TOKEN'))
