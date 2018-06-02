import discord
import fetcher
import chunker
import threading

def fetch():
    # do something here ...
    ff = fetcher.start_webdriver()
    ship_matrix = fetcher.get_ship_matrix(ff, fetcher.ship_matrix_URL)
    ships = fetcher.get_all_ships(ship_matrix)

    with open('fetched.txt', 'w') as f:
        f.write(ships)
        print("fetched ship matrix")

    threading.Timer(60, fetch).start()

client = discord.Client()

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
    if message.content.startswith('!dev_all_ships'):

        with open('fetched.txt') as f:
            ships = f.read()


        for chunk in chunker.split(ships, 2000):
            await client.send_message(message.channel, chunk)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

fetch()
client.run('NDUyMTk3NTk1OTUyMTg1MzU3.DfM61w.4CkpZGofxu7SBv9g8709b-GnBsY')