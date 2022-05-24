from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def drug_bank_init(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://go.drugbank.com/drug-interaction-checker")

def get_shortest_item(driver):
    count = 1
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'select2-results__option')]")))
        tmp = 1
        for item in driver.find_elements_by_xpath("//li[contains(@class, 'select2-results__option')]"):
            if len(item.text) < len(driver.find_element_by_xpath("//li[contains(@class, 'select2-results__option')][%s]"% str(count)).text):
                count = tmp
            tmp += 1
    except:
        return -1

    try:
        driver.find_element_by_xpath("//li[contains(@class, 'select2-results__option')][%s]"% str(count)).click()
    except:
        return -1

    return 0

def send_data(drug, driver):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='select2-search__field']"))).send_keys(drug)
    except:
        return -1

    while True:
        try:
            driver.find_element_by_xpath("//span[text()='Searching…']")
        except:
            break

    if get_shortest_item(driver) == -1:
        return -1
    else:
        return 0


def submit(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    except:
        return -1

def get_data(driver):
    try:
        result = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'severity-badge')]"))).text
        return result
    except:
        return -1

def drug_bank_input_data(drug1, drug2, driver):
    driver.switch_to.window(driver.window_handles[1])
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
