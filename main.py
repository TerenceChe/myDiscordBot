# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

from database import *
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

    # check price of a particular stock
    elif message.content.startswith('$$ price '):
        symbol = message.content.split()[2]
        await message.channel.send(all_info(symbol))
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

    elif message.content.startswith('$$ watchlist'):
        msg = message.content.split()
        uid = message.author.id
        if len(msg) == 2:
            cursor = get_watchlist(uid)
            if cursor.count() < 1:
                await message.channel.send("to add stocks to watchlist use command '$$ watchlist add <stock>'")
            for n in cursor:
                symbol = n.get('stock')
                await message.channel.send(all_info(symbol))
            return
        elif msg[2] == 'add':
            stock = msg[3]
            add_to_watch(uid, stock)
            await message.channel.send("successfully added {0} to watchlist".format(stock))
            return
        elif msg[2] in ['del', 'delete', 'remove']:
            stock = msg[3]
            remove_from_watch(uid, stock)
            await message.channel.send("successfully removed {0} from watchlist".format(stock))
            return

    elif message.content.startswith('$$ embed'):
        print(message)
        await message.channel.send(embed=embedMessage(message))
        return

client.run(os.getenv('TOKEN'))
