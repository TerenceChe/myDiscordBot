import discord


def embedMessage(message):
    embed = discord.Embed(title = "Sample Embed",
                          url = "https://google.ca",
                          description = "testing something",
                          color = 0x78AB46)
    embed.set_author(name = message.author.name, icon_url = message.author.avatar_url)
    return embed