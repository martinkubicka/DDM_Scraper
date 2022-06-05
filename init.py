## @file init.py
# @author Martin Kubička (xkubic45@stud.fit.vutbr.cz)
# @date 3.6.2022
#
# @brief declarations for functions which initializate browsers or files

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

## @brief function for opening browser
#
# @return driver opened window
def browser_init():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.set_window_size(1200, 1100)
    return driver

## @brief function for closing browser
#
# @param driver
def browser_dtor(driver):
    driver.quit()

## @brief function for opening/resetting files
#
# @return file_read file from where program reads data
def open_file():
    file_read = open("data.txt", "r")
    file_write = open("output.txt", "w")
    file_write.close()
    return file_read

## @brief funtion for closing file
#
# @param file_read file which will be closed
def file_dtor(file_read):
    file_read.close()

### End of init.py ###
