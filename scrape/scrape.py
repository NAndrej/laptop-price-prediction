
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
from itertools import cycle
import os
import random
import sys
import csv

class Scraper():

    def __init__(self):
        self.output = None
        self.user_agents = []
        self.driver = None
        self.base_urls = []
        self.curr_page = 0
        self.actions = None

    def write_csv(self,file,row):
        with open(file, "a", newline='', encoding="utf-8") as f:
            csv_writer = csv.writer(f,delimiter=',',quotechar='"')
            csv_writer.writerow(row)
    
    def load_useragents(self):
         with open("user_agents.txt", "r") as f:
            user_agents = f.readlines()
            self.user_agents = [i.strip().strip("\n") for i in user_agents]

    def load_baseurls(self):
        with open("base_urls.txt", "r") as f:
            b_urls = f.readlines()
            self.base_urls = [i.strip().strip("\n") for i in b_urls]

    def get_driver(self):
        
        user_agent = random.choice(self.user_agents)


        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent="+str(user_agent))
        # chrome_options.add_argument("proxy-server="+str(next(self.proxypool)))
        chrome_options.add_argument("headless")
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-logging")
        chrome_options.add_argument("log-level=3")
        
        self.driver = webdriver.Chrome(options=chrome_options,executable_path="c_driver/chromedriver.exe")
        self.actions = ActionChains(self.driver)

    def setup(self):
        self.output = os.path.join(os.getcwd(), "output.csv")
        self.write_csv(self.output,["NAME","CPU","GPU","DISPLAY","STORAGE","RAM","WEIGHT","PRICE($)","URL"])
        self.load_useragents()
        self.load_baseurls()
        self.get_driver()

    def scrape_urls(self,items_urls):
        for item_url in items_urls:
            print("Scraping " + item_url)
            self.driver.get(item_url)
            try:
                item_name = self.driver.find_element_by_xpath("//div[@class='lm-catalog-headline']//h1").text
            except:
                item_name = " "
            try:
                item_cpu = self.driver.find_element_by_class_name("cpu").text.split(":")[1].lstrip(" ")
            except:
                item_cpu = " "
            
            try:
                item_gpu = self.driver.find_element_by_class_name("gpu").text.split(":")[1].lstrip(" ")
            except:
                item_gpu = " "
            try:
                item_display = self.driver.find_element_by_class_name("display").text.split(":")[1].lstrip(" ")
            except:
                item_display = " "
            try:
                item_storage = self.driver.find_element_by_class_name("storage").text.split(":")[1].lstrip(" ")
            except:
                item_storage = " "
            try:
                item_ram = self.driver.find_element_by_class_name("ram").text.split(":")[1].lstrip(" ")
            except:
                item_ram = " "
            try:
                item_weight = self.driver.find_element_by_class_name("weight").text.split(":")[1].lstrip(" ")
            except:
                item_weight = " "
            try:
                item_price = self.driver.find_element_by_xpath("//a[contains(@class,'catalog-button-orange')]")

                if item_price.text.split("Buy")[0].strip("\n").rstrip(" ") == "Check Price":
                    print("Laptop without price found")
                    continue
                try:
                    item_price = item_price.find_element_by_tag_name("em")
                except:
                    item_price = item_price.text.split("Buy")[0].strip("\n").rstrip(" ").lstrip("$")
                else:
                    item_price = item_price.text.rstrip(" ").lstrip("$")
                    print("Sale found, new price is " + str(item_price))

            except:
                item_price = " "
            

            row = item_name,item_cpu,item_gpu,item_display,item_storage,item_ram,item_weight,item_price
            self.write_csv(self.output,row)


    def run(self):
               
        for b_url in self.base_urls:
            self.driver.get(b_url)
            s = b_url.split("5D=")
            range1 = s[1].split("&")[0]
            range2 = s[2].split("&")[0]
            print("Scraping: " + range2 + " - " + range1)
            
            WebDriverWait(self.driver,5).until(
                ec.presence_of_element_located((By.CLASS_NAME,'item-wrapper'))
            )

            items = self.driver.find_elements_by_class_name('item-wrapper')
            items_urls = [item.find_element_by_xpath(".//div[@class='item-title']/h5/a").get_attribute("href") for item in items]
            random_urls = random.sample(items_urls,200) # Random 200 for each price range
            
            self.scrape_urls(random_urls)

        

if __name__=="__main__":
    scr = Scraper()
    scr.setup()
    scr.run()
    

