from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"

print("target URL set to:", ship_matrix_URL)

print("setting headless arguments")
options = opts()
options.set_headless(headless=True)

print("setting webdriver")

ff = wd.Firefox(firefox_options=options)

print("waiting for get response...")

ff.get(ship_matrix_URL)

print("waiting for ship matrix to load...")

WebDriverWait(ff, 3).until(
    EC.presence_of_element_located((By.ID, 'statsruler-top')))

print("fetching all ships...")

elems = ff.find_element_by_id(
    "shipscontainer").find_elements_by_class_name("ship")

print(len(elems), "ships found:")

for elem in elems:
    # print(elems[0].get_attribute("innerHTML"))
    print(elem.find_element_by_class_name("title").get_attribute("innerText"), " - ",
          elem.find_element_by_class_name("production_status").get_attribute("innerText").strip())

ff.quit()
