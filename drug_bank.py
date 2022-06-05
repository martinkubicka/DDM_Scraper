## @file drug_bank.py
# @author Martin Kubička (xkubic45@stud.fit.vutbr.cz)
# @date 3.6.2022
#
# @brief declarations of functions which scrape data from drugbank website

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

## @brief intialization of tab with drugbank website
#
# @param driver
def drug_bank_init(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://go.drugbank.com/drug-interaction-checker")

## @brief function for getting the shortest item from dropdown menu
#
# @param driver
# @return int -1 if there was an error otherwise 0
def get_shortest_item(driver):
    count = 1 ## count for storing index of the shortest item
    ## if there is no results return -1
    try:
        driver.find_element_by_xpath("//li[contains(text(), 'Please enter')]")
        return -1
    except:
        pass

    try:
        ## searching for dropdown menu options
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'select2-results__option')]")))
        tmp = 1
        ## going through options
        for item in driver.find_elements_by_xpath("//li[contains(@class, 'select2-results__option')]"):
            if len(item.text) < len(driver.find_element_by_xpath("//li[contains(@class, 'select2-results__option')][%s]"% str(count)).text):
                count = tmp
            tmp += 1
    except:
        return -1

    ## select the shortest option
    try:
        driver.find_element_by_xpath("//li[contains(@class, 'select2-results__option')][%s]"% str(count)).click()
    except:
        return -1

    return 0

## @brief function for writing data to input box and then picking the shortest result
#
# @param drug name of drug which will be entered to input box
# @param driver
# @return int -1 if there was an error otherwise 0
def send_data(drug, driver):
    ## writing name of drug to input box
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='select2-search__field']"))).send_keys(drug)
    except:
        return -1

    count_reload = 0 ## count for how many reloads were executed
    while True: ## while website is searching for results
        if count_reload == 5: ## if there is still searching after 5 tries return -1
            return -1
        count_reload += 1
        try:
            driver.find_element_by_xpath("//span[text()='Searching…']")
            time.sleep(1)
        except:
            break

    if get_shortest_item(driver) == -1:
        return -1
    else:
        return 0

## @brief for clicking submit button after inputting drugs
#
# @param driver
# @return int -1 if there was an error otherwise 0
def submit(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        return 0
    except:
        return -1

## @brief function for getting severity of interaction
#
# @param driver
# @return result return severity or -1 if severity wasn't found
def get_data(driver):
    try:
        result = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'severity-badge')]"))).text
        return result
    except:
        return -1

## @brief main function of drugbank file
#
# @param drug1 name of first drug which will be entered to input box
# @param drug2 name of second drug which will be entered to input box
# @param driver
# @return result return severity or -1 if severity wasn't found
def drug_bank_input_data(drug1, drug2, driver):
    ## switch tabs
    driver.switch_to.window(driver.window_handles[1])
    ## reload site
    while True:
        try:
            driver.get("https://go.drugbank.com/drug-interaction-checker")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='navbar-brand']")))
            break
        except:
            pass

    if send_data(drug1, driver) == -1:
        return -1
    if send_data(drug2, driver) == -1:
        return -1

    if submit(driver) == -1:
        return -1

    result = get_data(driver)
    return result

### End of drug_bank.py ###
