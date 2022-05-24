from drugs import *
from medscape import *
from drug_bank import *

def write_data(line, arr, txt, drugbank, medscape):
    f = open("output.txt", "a")
    final_line = line.replace("\n", "")
    for i in arr:
        final_line = final_line + "#" + str(i)
    final_line = final_line + "#" + str(txt) + "#" + str(drugbank) + "#" + str(medscape) + "\n"
    f.write(final_line)
    f.close()

def get_data(driver, file_read):
    count_reload = 0
    for i in file_read.readlines():
        drugs_data = drugs_input_data(i.split("#")[1], i.split("#")[3], driver)

        medscape_data = medscape_input_data(i.split("#")[1], i.split("#")[3], driver, count_reload)
        count_reload += 1
        if count_reload == 6:
            count_reload = 0

        drug_bank_data = drug_bank_input_data(i.split("#")[1], i.split("#")[3], driver)

        if drugs_data == -1:
            write_data(i, [-1, -1, -1, -1, -1], -1, drug_bank_data, medscape_data)
        else:
            write_data(i, drugs_data[0], drugs_data[1], drug_bank_data, medscape_data)