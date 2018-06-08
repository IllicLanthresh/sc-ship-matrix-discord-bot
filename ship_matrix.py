from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
from jsondiff import diff
import asyncio


class ShipMatrix:

    def __init__(self, client):

        fetcher = ShipMatrixFetcher(client)

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

    def __init__(self, client):
        client.loop.create_task(self.fetch(client))

    async def fetch(self, client):

        while not client.is_closed:


        
            await client.wait_until_ready()

            ff = await self.start_webdriver()
            print("Started webdriver")

            raw_shipmatrix = await self.get_raw_shipmatrix(ff, self.ship_matrix_URL)
            
            if (raw_shipmatrix==None):
                print("Failed to connect to website, retry in 10 mins...")
                await asyncio.sleep(60*10)
                return
            print("Got shipmatrix in raw format")

            ships = self.raw_shipmatrix_to_json_string(raw_shipmatrix)
            print("Parsed all ships to json format")

            with open('fetched.json', 'r') as f:
                cached_ships = f.read()

            if (cached_ships != ships):
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
                cached_json = json.loads(cached_ships)
                ships_json = json.loads(ships)



                with open('fetched.json', 'w') as f:
                    f.write(ships)
                    print("Fetched all - cached into 'fetched.json'")
            else:
                print("No changes on ship matrix keep current chached version")

            await self.stop_webdriver(ff)
            print("Stopped webdriver")
            await asyncio.sleep(60*10)

    async def start_webdriver(self):

        options = opts()
        options.set_headless(headless=True)

        ff = wd.Firefox(firefox_options=options)

        print("Setted WebDriver Firefox as headless mode")

        return ff

    async def get_raw_shipmatrix(self, ff, url):

        try:
            ff.get(url)
            WebDriverWait(ff, 3).until(
                EC.presence_of_element_located((By.ID, 'statsruler-top')))
        except:
            self.stop_webdriver(ff)
            return
        ship_matrix = ff.find_element_by_id(
            "shipscontainer").find_elements_by_class_name("ship")

        return ship_matrix

    async def raw_shipmatrix_to_json_string(self, ship_matrix):

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
        return json.dumps(ships, indent=4)

    async def stop_webdriver(self, ff):
        ff.quit()
