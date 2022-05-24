from drugs import *
from init import *
from drug_bank import *
from medscape import *
from data import *

def main_init():
    driver = browser_init()
    files_array = open_file()

    drugs_init(driver)
    drug_bank_init(driver)
    medscape_init(driver)

    return driver, files_array

def main_dtor(driver, file):
    browser_dtor(driver)
    file_dtor(file)

def main():
    arr = main_init()

    get_data(arr[0], arr[1])

    main_dtor(arr[0], arr[1])

    print("Finished")
    input("Press enter to continue..")

if __name__ == '__main__':
    main()


