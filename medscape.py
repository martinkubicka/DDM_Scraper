from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import json

def medscape_init(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get("https://reference.medscape.com/drug-interactionchecker")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()

def get_shortest_item(driver):
    result = ""
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='MDICdrugs']/li/a")))
        time.sleep(1) #err + zle
        for item in driver.find_elements_by_xpath("//ul[@id='MDICdrugs']/li/a"):
            if result == "":
                result = item.get_attribute("href").split("(")[1].split(",")[0].replace("'", "")
            elif len(item.text) < len(result):
                result = item.get_attribute("href").split("(")[1].split(",")[0].replace("'", "")
    except:
        return -1

    return result

def get_id(drug, driver):
    try:
        elem = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='MDICtextbox']")))
        elem.send_keys(drug)
        elem.send_keys(" ")
        elem.send_keys(Keys.BACKSPACE)
    except:
        return -1

    id = get_shortest_item(driver)

    elem.clear()
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)

    return id

def medscape_input_data(drug1, drug2, driver, reload):
    driver.switch_to.window(driver.window_handles[2])

    if reload == 5:
        while True:
            try:
                driver.get("https://reference.medscape.com/drug-interactionchecker")
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Medscape Logo']")))
                break
            except:
                pass


    id1 = get_id(drug1, driver)
    if id1 == -1:
        return -1
    id2 = get_id(drug2, driver)
    if id2 == -1:
        return -1

    try:
        response = requests.get("https://reference.medscape.com/druginteraction.do?action=getMultiInteraction&ids=" + str(id1) + "," + str(id2))
        return json.loads(response.text)["multiInteractions"][0]["severity"]
    except:
        return -1











