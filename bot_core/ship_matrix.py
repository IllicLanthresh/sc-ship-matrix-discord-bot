"""
This module contains the ShipMatrix and ShipMatrixFetcher classes.

Only ShipMatrix is intended to be used. ShipMatrixFetcher is for internal usage of the module.
"""
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager


class ShipMatrix:
    """
    Class that automatically sets a matrix fetcher and can output a list of ships.

    Right now there are only two getters: get_all() and get_flight_ready().
    """

    def __init__(self):
        self.__fetcher = ShipMatrixFetcher()

    def get_fetcher(self):
        """
        Returns the instance of the fetcher.
        """
        return self.__fetcher

    def get_all(self):
        """
        Returns all ship entries in the matrix.
        """
        return self.__fetcher.get_fetched()

    def get_flight_ready(self):
        """
        Returns ship entries marked as flight ready in the matrix.
        """
        ships = self.__fetcher.get_fetched()

        filtered_ships = []
        for ship in ships:
            if ship['status'] == "Flight Ready":
                filtered_ships.append(ship)

        return filtered_ships


class ShipMatrixFetcher:
    """
    This class is the responsible for fetching all the ship data from the matrix on the website.
    """

    def __init__(self):
        self.__ship_matrix_url = "https://robertsspaceindustries.com/ship-matrix"
        self.__browser = self.__get_browser()
        self.__fetching_time_mins = 10
        self.__fetched = None

    def get_fetched(self):
        """
        Returns list of ships populated with every ship attribute.
        """
        return self.__fetched

    def register_to_loop(self, loop):
        """
        Registers the fetching method to an existing asyncio loop.
        """
        loop.create_task(self.__fetch())

    async def __fetch(self):
        while True:
            raw_shipmatrix = await self.__get_raw_shipmatrix()

            if raw_shipmatrix is None:
                print("Failed to connect to website, retry in " +
                      self.__fetching_time_mins + " mins...")
                await asyncio.sleep(self.__fetching_time_mins*60)
                continue
            print("Got shipmatrix in raw format")

            ships = await self.__parse_raw_ship_matrix(raw_shipmatrix)
            print("Parsed all ships")

            self.__fetched = ships
            print("Fetched all - cached in memory")

            await asyncio.sleep(self.__fetching_time_mins*60)

    def __get_browser(self):
        """
        Returns an instance of a chrome webdriver in headless mode.
        If the driver it's not installed it takes care of it.
        """
        print("Setting WebDriver Chrome as headless mode")
        options = chromeOptions()
        options.set_headless(headless=True)
        chrome = webdriver.Chrome(ChromeDriverManager().install(),
                                  chrome_options=options)
        return chrome

    async def __get_raw_shipmatrix(self):
        try:
            self.__browser.get(self.__ship_matrix_url)
            WebDriverWait(self.__browser, 3).until(
                EC.presence_of_element_located((By.ID, 'statsruler-top')))
        except Exception:
            return None

        ship_matrix = self.__browser.find_element_by_id(
            "shipscontainer").find_elements_by_class_name("ship")

        return ship_matrix

    async def __parse_raw_ship_matrix(self, ship_matrix):
        # TODO: Create Ship class instead of using a dictionary for every ship entry
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
        return ships
