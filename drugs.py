## @file drugs.py
# @author Martin Kubička (xkubic45@stud.fit.vutbr.cz)
# @date 3.6.2022
#
# @brief declarations of functions which scrape data from drugs website

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

## @brief function for initializating drugs website
#
# @param driver
def drugs_init(driver):
    driver.get("https://www.drugs.com/drug_interactions.html")
    try:
        ## accepting cookies
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Accept']"))).click()
        time.sleep(1)
    except:
        pass

## @brief function for getting href attribute (we can access drug interaction site faster and safer) of the shortest item from dropdown menu
#
# @param driver
# @return result href (id) of the shortest item or return -1 if there is no results
def get_shortest_result(driver):
    result = ""
    ## check if there is dropdown menu
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ls-item']")))
    except:
        return -1
    try:
        ## going through dropdown menu
        for item in driver.find_elements_by_xpath("//a[@class='ls-item']"):
            if result == "":
                result = item.get_attribute("href").split("?drug_list=")[1]
            elif len(item.text) < len(result):
                result = item.get_attribute("href").split("?drug_list=")[1]
    except:
        return -1

    return result

## @brief function for inputting a name of drug to input box and getting id of the drug
#
# @param drug name of drug
# @param driver
# @return link id of drug
def select_option(drug, driver):
    ## inputting drug name
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='livesearch-interaction-basic']"))).send_keys(drug)
    link = get_shortest_result(driver)
    if link == -1:
        return -1
    ## clearing input field
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='livesearch-interaction-basic']"))).clear()
    ## after clearing input field dropdown menu of results doesn't disappear so click somewhere to remove it
    driver.find_element_by_tag_name("p").click()

    return link

## @brief function for opening interaction site of two drugs
#
# @param drug1 id of the first drug
# @param drug2 id of the second drug
# @param driver
# @return arr,txt arr->array of results (ints) and txt-> text from website (MONITOR CLOSELY...)
def open_interaction_site(drug1, drug2, driver):
    arr = []
    txt = -1

    count_reload = 0 ## counting how much times site was reloaded
    ## accessing interaction site
    while True:
        try:
            if count_reload == 5:
                return -1, -1
            count_reload += 1
            driver.get("https://www.drugs.com/interactions-check.php?drug_list=" + drug1 + "," + drug2)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//h1[text()='Drug Interaction Report']")))
            break
        except:
            pass

    try:
        # click on professional button
        elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Professional']")))
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        elem.click()

        ## scraping wanter results and adding them to array which will be returned
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ddc-form-check']")))
        for i in driver.find_elements_by_xpath("//form[@id='filterSection']/div[@class='ddc-form-check']/label/span"):
            arr.append(i.text.split("(")[1].replace(")", ""))
    except:
        return -1, -1

    ## scraping text (for example MONITOR CLOSELY...)
    # we know if there are first three elements of array equal to zero then there will be no or unwanted text
    if arr[0] != 0 and arr[1] != 0 and arr[2] != 0:
        try:
            txt = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='interactions-reference']/p"))).text.split(":")[0]
            if txt.isupper() == False:
                txt = -1
        except:
            pass
    else:
        txt = -1
    return arr, txt

## @brief main function for scraping drugs website
#
# @param drug1 name of first drug
# @param drug2 name of second drug
# @param driver
# @return data it is array of another array and scraped text data = [arr, txt] or return -1 if something goes wrong
def drugs_input_data(drug1, drug2, driver):
    ## switch tabs
    driver.switch_to.window(driver.window_handles[0])
    ## load site
    while True:
        try:
            driver.get("https://www.drugs.com/drug_interactions.html")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//h1[text()='Drug Interactions Checker']")))
            break
        except:
            pass

    ## get id of first drug
    ret1 = select_option(drug1, driver)
    if ret1 == -1:
        return -1

    ## get id of second drug
    ret2 = select_option(drug2, driver)
    if ret2 == -1:
        return -1

    ## get results
    data = open_interaction_site(ret1, ret2, driver)
    if data[0] == -1:
        return -1

    return data

### End of drugs.py ###
