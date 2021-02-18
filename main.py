# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

import discord
import os
from stockInfo import *

client = discord.Client()

url = 'https://finance.yahoo.com/gainers/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
mostGain = soup.findAll('tr')[1]

for child in mostGain.children:
	print(child)
	print(" ")


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	# do not read messages from itself
	if message.author == client.user:
		return

	# gives the command to play David's playlist
	if message.content.startswith('$David'):
		await message.channel.send(
		    '-p https://open.spotify.com/playlist/2pOCpGDfekUKDN6Mzr1NGi')

	if message.content.startswith('$mostgain'):
		await message.channel.send(mostGain())

	if message.content.startswith('$mostloss'):
		await message.channel.send(mostLoss())


client.run(os.getenv('TOKEN'))
