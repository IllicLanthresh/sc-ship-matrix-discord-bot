from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options as opts

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ship_matrix_URL = "https://robertsspaceindustries.com/ship-matrix"

print("target URL set to:", ship_matrix_URL)

#print("seting headless arguments")
options = opts()
#options.set_headless(headless=True)

print("setting firefox driver")

ff = wd.Firefox(firefox_options=options)

print("loading...")

ff.get(ship_matrix_URL)

print("waiting for ship matrix to load...")

WebDriverWait(ff, 3).until(EC.presence_of_element_located((By.ID, 'statsruler-top')))

print("get all ships")

elems = ff.find_element_by_id("shipscontainer").find_elements_by_class_name("ship")

print(len(elems), "ships found")

last_elem_text = elems[len(elems)-1].get_attribute("innerText")

elems_loaded = 0



while elems_loaded < len(elems):
    elems = ff.find_element_by_id("shipscontainer").find_elements_by_class_name("ship")
    last_elem_text = elems[len(elems)-1].get_attribute("innerText")

    var = 0
    for elem in elems:
        if elem.get_attribute("innerText") != "":
            var += 1
    elems_loaded = var

    print("\rships loaded:", elems_loaded, end="")
print("")

#for elem in elems:
#    print(elem.get_attribute("innerText"))
#    print(elem.tag_name)


ff.quit()