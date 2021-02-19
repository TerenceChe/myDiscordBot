import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import yfinance as yf


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

def currentPrice(symbol):
    if symbol == "DAVID":
        return "FREE"
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        return data['Close'][0]
    except:
        return "could not find symbol"