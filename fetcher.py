from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"

def start_webdriver():
    #print("target URL set to:", url)

    #print("setting headless arguments")
    options = opts()
    options.set_headless(headless=True)

    #print("setting webdriver")

    ff = wd.Firefox(firefox_options=options)

    return ff

def get_ship_matrix(ff, url):
    #print("waiting for get response...")

    ff.get(url)

    #print("waiting for ship matrix to load...")

    WebDriverWait(ff, 3).until(
        EC.presence_of_element_located((By.ID, 'statsruler-top')))

    #print("fetching all ships...")

    ship_matrix = ff.find_element_by_id(
        "shipscontainer").find_elements_by_class_name("ship")

    #print(len(ships), "ships found:")
    return ship_matrix

def stop_webdriver(ff):
    ff.quit()

def get_all_ships(ship_matrix):
    ships = ""
    for ship in ship_matrix:
        # print(ships[0].get_attribute("innerHTML"))
        ships += ship.find_element_by_class_name("title").get_attribute("innerText")
        ships += " - "
        ships += ship.find_element_by_class_name("production_status").get_attribute("innerText").strip()
        ships += "\n"
    return ships
