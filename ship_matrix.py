from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
from jsondiff import diff
import asyncio


class ShipMatrix:
    fetcher = None

    def __init__(self, client):

        self.fetcher = ShipMatrixFetcher(client)

    def getAll(self):

        return self.fetcher.fetched

    def getFlightReady(self):

        filtered_ships = []
        for ship in self.fetcher.fetched:
            if (ship['status'] == "Flight Ready"):
                filtered_ships.append(ship)

        return filtered_ships


class ShipMatrixFetcher:
    
    ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"
    ff = None
    client = None
    fetched = None
    fetchedTimeMins = 10

    def __init__(self, discordclient):
        client = discordclient
        self.ff = self.start_webdriver()
        print("Started webdriver")
        client.loop.create_task(self.fetch()) #TODO: move this to 'discord-bot.py', passing 'fetch()' function pointer to it using function pointer variable on 'ShipMatrix' called 'fetchFP', then execute 'client.run()' BEFORE this

    async def fetch(self):

        while not self.client.is_closed:

            await self.client.wait_until_ready()

            raw_shipmatrix = await self.get_raw_shipmatrix()

            await self.client.wait_until_ready()

            if (raw_shipmatrix == None):
                print("Failed to connect to website, retry in " +
                      self.fetchedTimeMins + " mins...")
                await asyncio.sleep(self.fetchedTimeMins*60)
                continue
            print("Got shipmatrix in raw format")

            ships = self.raw_shipmatrix_to_json(raw_shipmatrix)
            print("Parsed all ships to json format")

            if (self.fetched != ships):
                # print(json.dumps(json.loads(diff(a,b, load=False, dump=True)),indent=4))
                #changes on shipmatrix, TODO:look for changes and send msg to discord
                #       "{'0': {'$delete': ['link']}, '1': {'status': 'In Concept', '$delete': ['link']}}
                #        >>> print(json.dumps(c, indent=4))
                #        {
                #            "0": {
                #                "$delete": [
                #                    "link"
                #                ]
                #            },
                #            "1": {
                #                "status": "In Concept",
                #                "$delete": [
                #                    "link"
                #                ]
                #            }
                #        }"
                
                ######################################## TODO TODO TODO!!!! use DeepDiff!!!!

                self.fetched    #cached_json
                ships           #ships_json

                self.fetched = ships
                print("Fetched all - cached in memory")
            else:
                print("No changes on ship matrix keep current chached version")

            await asyncio.sleep(self.fetchedTimeMins*60)
        print("discord client is closed")

    def start_webdriver(self):

        options = opts()
        options.set_headless(headless=True)

        firefox = wd.Firefox(firefox_options=options)

        print("Setted WebDriver Firefox as headless mode")

        return firefox

    async def get_raw_shipmatrix(self):

        try:
            self.ff.get(self.ship_matrix_URL)
            WebDriverWait(self.ff, 3).until(
                EC.presence_of_element_located((By.ID, 'statsruler-top')))
        except:
            return

        ship_matrix = self.ff.find_element_by_id(
            "shipscontainer").find_elements_by_class_name("ship")

        return ship_matrix

    async def raw_shipmatrix_to_json(self, ship_matrix):

        ships = []
        for ship in ship_matrix:
            dict_entry = {}

            dict_entry['name'] = ship.find_element_by_class_name(
                "title").get_attribute("innerText").strip()

            dict_entry['status'] = ship.find_element_by_class_name(
                "production_status").get_attribute("innerText").strip()

            dict_entry['link'] = ship.find_element_by_class_name("actionscontainer").find_element_by_class_name(
                "statbox").find_element_by_class_name("other").get_attribute("href")

            ships.append(dict_entry)
            await self.client.wait_until_ready()
        return ships

    async def stop_webdriver(self, ff):
        ff.quit()
