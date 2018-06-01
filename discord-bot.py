import discord
import fetcher

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!hammerhead'):
        msg = 'rat1on thinks the hammerhead it\'s beautiful'
        await client.send_message(message.channel, msg)
    if message.content.startswith('!all_ships'):
        await client.send_message(message.channel, "gimme a second...")
        ff = fetcher.start_webdriver()
        ship_matrix = fetcher.get_ship_matrix(ff, fetcher.ship_matrix_URL)
        await client.send_message(message.channel, "almost finished...")
        ships = fetcher.get_all_ships(ship_matrix)
        await client.send_message(message.channel, "there u go:")

        

        for chunk in [ships[i:i+2000] for i in range(0, len(ships), 2000)]:
            await client.send_message(message.channel, chunk)
            print(chunk)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('NDUyMTk3NTk1OTUyMTg1MzU3.DfM61w.4CkpZGofxu7SBv9g8709b-GnBsY')