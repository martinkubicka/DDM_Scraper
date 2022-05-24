from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def browser_init():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.set_window_size(1200, 1100)
    return driver

def browser_dtor(driver):
    driver.quit()

def open_file():
    file_read = open("data.txt", "r")
    file_write = open("output.txt", "w")
    file_write.close()
    return file_read

def file_dtor(file_read):
    file_read.close()
