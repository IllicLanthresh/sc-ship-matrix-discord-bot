import discord
from ship_matrix import ShipMatrix
import chunker


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!hammerhead'):
        msg = 'rat1on thinks the hammerhead it\'s beautiful'
        await client.send_message(message.channel, msg)
    if message.content.startswith('!all_ships'):
        ships = matrix.getAll()
        msg = ""

        for ship in ships:
            msg += "%(name)s:\n\tStatus: %(status)s\n\tlink: %(link)s\n" % ship

        for chunk in chunker.make_chunks(message, 2000):
            await client.send_message(message.channel, chunk)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client = discord.Client()
matrix = ShipMatrix()
client.run('NDUyMTk3NTk1OTUyMTg1MzU3.DfM61w.4CkpZGofxu7SBv9g8709b-GnBsY')