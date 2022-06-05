## @file data.py
# @author Martin Kubička (xkubic45@stud.fit.vutbr.cz)
# @date 3.6.2022
#
# @brief declarations of functions which are getting and then writing data from scraped sites

from drugs import *
# from medscape import *
from drug_bank import *
from init import *


## @brief function for writing scraped data
#
# @param line original line from file which is read
# @param arr array of results from drugs website
# @param txt text scraped from drugs website (MONITOR CLOSELY...)
# @param drugbank severity scraped from drugbank website
def write_data(line, arr, txt, drugbank): # add medscape here if you want to scrape it
    f = open("output.txt", "a")
    final_line = line.replace("\n", "")
    for i in arr:
        final_line = final_line + "#" + str(i)
    final_line = final_line + "#" + str(txt) + "#" + str(drugbank) + "\n" # add medscape here if you want to scrape it
    f.write(final_line)
    f.close()

## @brief function for getting data from all 2/3 websites
#
# @param driver
# @param file_read file from which data are read
# @return driver
def get_data(driver, file_read):
    # count_reload = 0 # medscape
    count = 0 ## counting how many drugs were scraped
    for i in file_read.readlines(): ## going through all lines
        if count == 1000: ## if 1000 drugs were scraped restart browser
            count = 0
            browser_dtor(driver)
            driver = browser_init()
            drugs_init(driver)
            drug_bank_init(driver)

        ## unwated lines -> continue
        if i == "\n":
            continue
        elif i.split("#")[1] == i.split("#")[3] or i.split("#")[1] == "" or i.split("#")[3] == "" or i.split("#")[1] in i.split("#")[3] or i.split("#")[3] in i.split("#")[1]:
            write_data(i, [-1, -1, -1, -1, -1], -1, -1)
            continue

        drugs_data = drugs_input_data(i.split("#")[1], i.split("#")[3], driver)

        # medscape_data = medscape_input_data(i.split("#")[1], i.split("#")[3], driver, count_reload)
        # count_reload += 1
        # if count_reload == 6:
        #     count_reload = 0

        drug_bank_data = drug_bank_input_data(i.split("#")[1], i.split("#")[3], driver)

        if drugs_data == -1:
            write_data(i, [-1, -1, -1, -1, -1], -1, drug_bank_data)
        else:
            write_data(i, drugs_data[0], drugs_data[1], drug_bank_data)

        count += 1
    return driver

### End of data.py ###
