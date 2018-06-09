from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import asyncio


class ShipMatrix:

    def __init__(self, client):

        fetcher = ShipMatrixFetcher(client) #TODO: use files only as backup at startup and use fetcher class to store the actual json object

    def getAll(self):
        with open('fetched.json') as f:
            ships = json.load(f)
        return ships
    def getFlightReady(self):
        with open('fetched.json') as f:
            ships = json.load(f)
        
        filtered_ships = []
        for ship in ships:
            if (ship['status'] == "Flight Ready"): filtered_ships.append(ship)

        return filtered_ships


class ShipMatrixFetcher:

    ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"
    ff = None
    client = None

    def __init__(self, discordclient):
        global ff
        global client
        client = discordclient
        ff = self.start_webdriver()
        print("Started webdriver")
        client.loop.create_task(self.fetch())

    async def fetch(self):
        global ff
        global client

        while not client.is_closed:

            await client.wait_until_ready()

            raw_shipmatrix = await self.get_raw_shipmatrix()
            
            if (raw_shipmatrix==None):
                print("Failed to connect to website, retry in 10 mins...")
                await asyncio.sleep(30)
                continue
            print("Got shipmatrix in raw format")

            ships = await self.raw_shipmatrix_to_json(raw_shipmatrix)
            print("Parsed all ships to json format")

            with open('fetched.json', 'w') as f:
                f.write(ships)
                print("Fetched all - cached into 'fetched.json'")

            # await self.stop_webdriver(ff)
            # print("Stopped webdriver")
            await asyncio.sleep(30)
        print("discord client is closed")

    def start_webdriver(self):

        options = opts()
        options.set_headless(headless=True)

        firefox = wd.Firefox(firefox_options=options)

        print("Setted WebDriver Firefox as headless mode")

        return firefox

    async def get_raw_shipmatrix(self):
        global ff

        try:
            ff.get(self.ship_matrix_URL)
            WebDriverWait(ff, 3).until(
                EC.presence_of_element_located((By.ID, 'statsruler-top')))
        except:
            # await self.stop_webdriver(ff)
            return
        await client.wait_until_ready()
        ship_matrix = ff.find_element_by_id(
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
            await client.wait_until_ready()
        return json.dumps(ships, indent=4)

    async def stop_webdriver(self, ff):
        ff.quit()
