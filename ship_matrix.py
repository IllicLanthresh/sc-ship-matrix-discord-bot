from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import threading
import json


class ShipMatrix:

    def __init__(self):

        fetcher = ShipMatrixFetcher()

        fetcher.fetch()

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

    def fetch(self):

        ff = self.start_webdriver()
        print("Started webdriver")

        raw_shipmatrix = self.get_raw_shipmatrix(ff, self.ship_matrix_URL)
        print("Got shipmatrix in raw format")

        ships = self.raw_shipmatrix_to_json(raw_shipmatrix)
        print("Parsed all ships to json format")

        with open('fetched.json', 'w') as f:
            f.write(ships)
            print("Fetched all - cached into 'fetched.json'")

        self.stop_webdriver(ff)
        print("Stopped webdriver")
        self.start_timmed_fether()

    def start_timmed_fether(self):
        threading.Timer(60*10, self.fetch).start()
        print("Setted new timed thread")
        print('------')

    def start_webdriver(self):

        options = opts()
        options.set_headless(headless=True)

        ff = wd.Firefox(firefox_options=options)

        print("Setted WebDriver Firefox as headless mode")

        return ff

    def get_raw_shipmatrix(self, ff, url):

        ff.get(url)

        WebDriverWait(ff, 3).until(
            EC.presence_of_element_located((By.ID, 'statsruler-top')))

        ship_matrix = ff.find_element_by_id(
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
