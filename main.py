from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
load_dotenv()

class car_container:
    def __init__(self):
        self.name   = ""
        self.href   = ""
        self.price  = ""
        self.loc    = ""
        self.specs  = ""
        self.km     = ""
        self.hp     = ""
    def __str__(self):
        return '''
Nume: {}
Link: {}
Pret: {}
Locatie: {}
Specificatii: {}
Km : {}
Hp: {}
'''.format(self.name, self.href, self.price, self.loc, self.specs, self.km, self.hp)



rootSite = "https://www.mobile.de"
site_to_scrape= os.environ.get("site_to_scrape")
googleFormLink = os.environ.get("googleFormLink")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(site_to_scrape)
driver.maximize_window()
items = str(driver.find_element_by_xpath("/html/body/div/div/div[3]/section/section[1]/div/h1").text)
myCars = []
totalSearchResult = int(items.split()[0])
searchedItems = 10
while True:

    site_html = driver.page_source
    soup = BeautifulSoup(site_html, 'html.parser')
    for soupItem in soup.find_all(class_="vehicle-data"):
        myCar = car_container()
        #vehicleTextSoup = soup.find(class_="vehicle-text")
        #print(soupItem.prettify())
        myCar.name = soupItem.find(class_="vehicle-title").text
        myCar.href = rootSite + str(soupItem['href'])
        myCar.loc   =  soupItem.find(class_="u-margin-bottom-9").text
        myCar.specs = soupItem.find(class_="vehicle-techspecs").text
        myCar.price = soupItem.find(class_="seller-currency").text
        vehicInfo = soupItem.find(class_="vehicle-information")
        myCar.km    = vehicInfo.find(class_="u-text-bold").text
        myCar.hp    = vehicInfo.find(class_="u-text-grey-60").text
        myCars.append(myCar)
        #print(str(myCar))
        # print("Price " + myCar.price)
        # print("Specs " + myCar.specs)
        # print("Km " + myCar.km)
        # print("hp " + myCar.hp)

    try:
        btn_to_clk = driver.find_element_by_xpath("/html/body/div/div/div[3]/section/section[2]/div/div[1]/a[2]")
    except:
        btn_to_clk = driver.find_element_by_xpath("/html/body/div/div/div[3]/section/section[2]/div/div[1]/a")
    driver.execute_script("arguments[0].click();", btn_to_clk)
    if(searchedItems >= totalSearchResult):
        break

    else:
        time.sleep(3)
        searchedItems += 10

#now fill the form
def sendKey(driver, xpath, key):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)))
    element.send_keys(key)
def clickElement(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)))
    element.click()


driver.get(googleFormLink)
for car in myCars:
    sendKey(driver,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea', car.name )
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea', car.href)
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input', car.price)
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input', car.loc)
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea', car.specs)
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input', car.km)
    sendKey(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input', car.hp)
    time.sleep(1)
    clickElement(driver, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    clickElement(driver, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')



driver.close()