## @file main.py
# @author Martin Kubička (xkubic45@stud.fit.vutbr.cz)
# @date 3.6.2022
#
# @brief declaration of main function which calls constructor and destructor functions

from drugs import *
from init import *
from drug_bank import *
from medscape import *
from data import *

## @brief initialization
#
# @return driver 
# @return file file from which program reads data
def main_init():
    driver = browser_init()
    file = open_file()

    drugs_init(driver)
    drug_bank_init(driver)
    #medscape_init(driver)

    return driver, file

## @brief destructor
#
# @param driver
# @param file file from which program reads data
def main_dtor(driver, file):
    browser_dtor(driver)
    file_dtor(file)

def main():
    arr = main_init()

    driver = get_data(arr[0], arr[1])

    main_dtor(driver, arr[1])

    print("Finished")
    input("Press enter to continue..")

if __name__ == '__main__':
    main()

### End of main.py ###
