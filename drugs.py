from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def drugs_init(driver):
    driver.get("https://www.drugs.com/drug_interactions.html")
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Accept']"))).click()
        time.sleep(1)
    except:
        pass

def get_shortest_result(driver):
    result = ""
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ls-item']")))
    except:
        return -1
    for item in driver.find_elements_by_xpath("//a[@class='ls-item']"):
        if result == "":
            result = item.get_attribute("href").split("?drug_list=")[1]
        elif len(item.text) < len(result):
            result = item.get_attribute("href").split("?drug_list=")[1]

    return result

def select_option(drug, driver):
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='livesearch-interaction-basic']"))).send_keys(drug)
    link = get_shortest_result(driver)
    if link == -1:
        return -1
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='livesearch-interaction-basic']"))).clear()
    driver.find_element_by_tag_name("body").click()

    return link

def open_interaction_site(drug1, drug2, driver):
    arr = []
    txt = -1

    while True:
        try:
            driver.get("https://www.drugs.com/interactions-check.php?drug_list=" + drug1 + "," + drug2)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//h1[text()='Drug Interaction Report']")))
            break
        except:
            pass

    try:
        elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Professional']")))
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        elem.click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ddc-form-check']")))
        count = 0
        for i in driver.find_elements_by_xpath("//form[@id='filterSection']/div[@class='ddc-form-check']/label/span"):
            arr.append(i.text.split("(")[1].replace(")", ""))
    except:
        return -1, -1

    try:
        txt = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='interactions-reference']/p"))).text.split(":")[0]
        if txt.isupper() == False:
            txt = -1
    except:
        pass
    return arr, txt

def drugs_input_data(drug1, drug2, driver):
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            driver.get("https://www.drugs.com/drug_interactions.html")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//h1[text()='Drug Interactions Checker']")))
            break
        except:
            pass

    ret1 = select_option(drug1, driver)
    if ret1 == -1:
        return -1
    ret2 = select_option(drug2, driver)
    if ret2 == -1:
        return -1

    data = open_interaction_site(ret1, ret2, driver)
    if data[0] == -1:
        return -1

    return data