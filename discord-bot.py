import discord
import fetcher
import chunker
import threading

def fetch_all():
    
    ff = fetcher.start_webdriver()
    print("started webdriver")
    ship_matrix = fetcher.get_ship_matrix(ff, fetcher.ship_matrix_URL)
    print("got shipmatrix")
    ships = fetcher.get_all_ships(ship_matrix)
    print("got all ships")

    with open('fetched_all.txt', 'w') as f:
        f.write(ships)
        print("fetched all - saved into 'fetched_all.txt'")

    fetcher.stop_webdriver(ff)
    print("stopped webdriver")
    threading.Timer(60*10, fetch_all).start()
    print("setted new timed thread")
    print('------')

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
    if message.content.startswith('!all_ships'):
        with open('fetched_all.txt') as f:
            ships = f.read()
        for chunk in chunker.split(ships, 2000):
            await client.send_message(message.channel, chunk)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

fetch_all()
client.run('NDUyMTk3NTk1OTUyMTg1MzU3.DfM61w.4CkpZGofxu7SBv9g8709b-GnBsY')