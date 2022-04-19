
from tkinter import E
from selenium import webdriver

def prepareGENEFileFromAccnNum(accnNum:str):

    driver=webdriver.Chrome('./chromedriver')
    driver.get("https://www.python.org")
    print(driver.title)



# #################################################

prepareGENEFileFromAccnNum("")