import requests
import urllib.request
import time
from bs4 import BeautifulSoup

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