from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from threading import Timer

import json


class ShipMatrix:
    global fetcher  # TODO: change to private

    def __init__(self, client):
        global fetcher

        # TODO: use files only as backup at startup and use fetcher class to store the actual json object
        fetcher = ShipMatrixFetcher(client)

    def getAll(self):
        global fetcher
        # with open('fetched.json') as f:
        #     ships = json.load(f)
        ships = json.loads(fetcher.fetched)
        return ships

    def getFlightReady(self):
        # with open('fetched.json') as f:
        #     ships = json.load(f)
        ships = json.loads(fetcher.fetched)

        filtered_ships = []
        for ship in ships:
            if (ship['status'] == "Flight Ready"):
                filtered_ships.append(ship)

        return filtered_ships


class ShipMatrixFetcher:
    
    ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"
    ff = None
    client = None
    fetched = None
    minsBetweenFetch = 10

    def __init__(self, discordclient):
        self.client = discordclient
        self.ff = self.start_webdriver()
        print("Started webdriver")
        self.fetch() #TODO: move this to 'discord-bot.py', passing 'fetch()' function pointer to it using function pointer variable on 'ShipMatrix' called 'fetchFP', then execute 'client.run()' BEFORE this ---MAYBE THIS IS USELESS NOW THAT WE USE THREADS

    def fetch(self):
        raw_shipmatrix = self.get_raw_shipmatrix()

        if (raw_shipmatrix == None):
            print("Failed to connect to website, retry in " +
                    self.minsBetweenFetch + " mins...")
            Timer(60*self.minsBetweenFetch, self.fetch).start()
            return
        print("Got shipmatrix in raw format")

        ships = self.raw_shipmatrix_to_json(raw_shipmatrix)
        print("Parsed all ships to json format")

        # with open('fetched.json', 'w') as f:
        #     f.write(ships)
        #     print("Fetched all - cached into 'fetched.json'")

        self.fetched = ships
        print("Fetched all - cached in memory")

        # self.stop_webdriver(ff)
        # print("Stopped webdriver")
        Timer(60*self.minsBetweenFetch, self.fetch).start()
        

    def start_webdriver(self):

        options = opts()
        options.set_headless(headless=True)

        firefox = wd.Firefox(firefox_options=options)

        print("Setted WebDriver Firefox as headless mode")

        return firefox

    def get_raw_shipmatrix(self):

        try:
            self.ff.get(self.ship_matrix_URL)
            WebDriverWait(self.ff, 3).until(
                EC.presence_of_element_located((By.ID, 'statsruler-top')))
        except:
            # self.stop_webdriver(ff)
            return

        ship_matrix = self.ff.find_element_by_id(
            "shipscontainer").find_elements_by_class_name("ship")

        return ship_matrix

    def raw_shipmatrix_to_json(self, ship_matrix):
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

    def stop_webdriver(self, ff):
        ff.quit()
