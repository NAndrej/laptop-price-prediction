
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
import pandas as pd

class Scraper():

    def __init__(self):
        self.output = None
        self.user_agents = []
        self.driver = None
        self.actions = None
        self.data_path = "../../data/data.csv"
        self.init_link = "https://www.techpowerup.com/cpu-specs/"
        self.cpu_list = None

    def load_useragents(self):
         with open("../user_agents.txt", "r") as f:
            user_agents = f.readlines()
            self.user_agents = [i.strip().strip("\n") for i in user_agents]

    def write_csv(self,file,row):
        with open(file, "a", newline='', encoding="utf-8") as f:
            csv_writer = csv.writer(f,delimiter=',',quotechar='"')
            csv_writer.writerow(row)
    
    def get_driver(self):
        
        user_agent = random.choice(self.user_agents)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent="+str(user_agent))
        # chrome_options.add_argument("proxy-server="+str(next(self.proxypool)))
        # chrome_options.add_argument("headless")
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-logging")
        chrome_options.add_argument("log-level=3")
        
        self.driver = webdriver.Chrome(options=chrome_options,executable_path="../c_driver/chromedriver.exe")
        self.actions = ActionChains(self.driver)

    def setup(self):
        self.cpu_list = pd.read_csv(self.data_path)["CPU"]
        self.load_useragents()
        self.get_driver()

    def run(self):
        self.driver.get(self.init_link)

        for cpu_name in self.cpu_list:
            print(cpu_name)
            self.driver.find_element_by_id("quicksearch").send_keys(cpu_name)
            time.sleep(1)



        
if __name__=="__main__":
    # scr = Scraper()
    # scr.setup()
    # scr.run()
    data = pd.read_csv("../../data/data.csv")
    print(data["GPU"].unique())
    

