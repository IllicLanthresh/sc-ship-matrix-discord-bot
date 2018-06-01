ships = (
    "https://robertsspaceindustries.com/pledge/ships/orion/Orion",
    "https://robertsspaceindustries.com/pledge/ships/anvil-hornet/F7C-Hornet",
    "https://robertsspaceindustries.com/pledge/ships/rsi-constellation/Constellation-Taurus"
)

from sys import argv
from pyquery import PyQuery as pq
import requests

print(argv)
def get_ship_status(shipURL):
    r = requests.get(shipURL)

    jq = pq(r.text)

    prod_status_div = jq("div.prod-status")

    titles_div = jq("div.titles > h1")

    titles_div.children().remove()

    shipNAME = titles_div.text().strip()

    print(shipNAME + ":")

    for children in prod_status_div.children():
        print("\t" + str(children.text))

for ship in ships:
    get_ship_status(ship)
