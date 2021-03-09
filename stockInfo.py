import datetime
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import sys


def most_gain():
    url = 'https://finance.yahoo.com/gainers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mostGain = soup.findAll('tr')[1]

    name = mostGain.a
    return name.string


def most_loss():
    url = 'https://finance.yahoo.com/losers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mostLoss = soup.findAll('tr')[1]

    name = mostLoss.a
    return name.string


def prev_close_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='2d')
        return data['Close'][0]
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def current_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        return data['Close'][0]
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def one_day_price_change(symbol):
    try:
        change = current_price(symbol) - prev_close_price(symbol)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    change = round(change, 2)
    if change > 0:
        change = "+" + str(change)
    return change


def change_percent(symbol):
    try:
        change = float(one_day_price_change(symbol))
        price = prev_close_price(symbol)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    percent = change / price
    percent *= 100
    return round(percent, 2)

def all_info(symbol):
    price = current_price(symbol)
    if price is None:
        return "symbol not found"

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
    return msg
