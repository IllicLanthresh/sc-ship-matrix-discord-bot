import discord
from ship_matrix import ShipMatrix
import chunker

client = discord.Client()
matrix = ShipMatrix(client)

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        msg = 'list of commands:\n\t!hello\n\t!hammerhead\n\t!all ships\n\t!flight ready'
        await client.send_message(message.channel, msg)
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!hammerhead'):
        msg = 'rat1on thinks the hammerhead it\'s beautiful'
        await client.send_message(message.channel, msg)
    if message.content.startswith('!all ships'):
        msg = ""

        for ship in matrix.getAll():
            msg += "%(name)s:\n\tStatus: %(status)s\n\tlink: <%(link)s>\n" % ship

        for chunk in chunker.make_chunks(msg, 2000):
            await client.send_message(message.channel, chunk)
    if message.content.startswith('!flight ready'):
        msg = "Flight Ready ships list:\n\n\n"

        for ship in matrix.getFlightReady():
            msg += "%(name)s:\n\tlink: <%(link)s>\n" % ship

        for chunk in chunker.make_chunks(msg, 2000):
            await client.send_message(message.channel, chunk)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run('***REMOVED***')