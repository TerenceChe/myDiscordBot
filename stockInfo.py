import requests
from bs4 import BeautifulSoup
import yfinance as yf
import sys

def mostGain():
    url = 'https://finance.yahoo.com/gainers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mostGain = soup.findAll('tr')[1]

    name = mostGain.a
    return name.string


def mostLoss():
    url = 'https://finance.yahoo.com/losers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    mostLoss = soup.findAll('tr')[1]

    name = mostLoss.a
    return name.string

def prevClosePrice(symbol):
    try:
      ticker = yf.Ticker(symbol)
      data = ticker.history(period='2d')
      return data['Close'][0]
    except:
      return print("Unexpected error:", sys.exc_info()[0])
      raise

def currentPrice(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        return round(data['Close'][0], 2)
    except:
        return print("Unexpected error:", sys.exc_info()[0])
        raise


def oneDayPriceChange(symbol):
    try:
        change = currentPrice(symbol) - prevClosePrice(symbol)
    except:
        return print("Unexpected error:", sys.exc_info()[0])
        raise

    change = round(change, 2)
    if change > 0:
        change = "+" + str(change)
    return change

def changePercent(symbol):
    try:
        change = float(oneDayPriceChange(symbol))
        price = prevClosePrice(symbol)
    except:
        return print("Unexpected error:", sys.exc_info()[0])
        raise

    percent = change / price
    percent *= 100
    return round(percent, 2)