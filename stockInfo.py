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
        return print("Unexpected error:", sys.exc_info()[0])


def current_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        return data['Close'][0]
    except:
        return print("Unexpected error:", sys.exc_info()[0])


def one_day_price_change(symbol):
    try:
        change = current_price(symbol) - prev_close_price(symbol)
    except:
        return print("Unexpected error:", sys.exc_info()[0])

    change = round(change, 2)
    if change > 0:
        change = "+" + str(change)
    return change


def change_percent(symbol):
    try:
        change = float(one_day_price_change(symbol))
        price = prev_close_price(symbol)
    except:
        return print("Unexpected error:", sys.exc_info()[0])

    percent = change / price
    percent *= 100
    return round(percent, 2)
