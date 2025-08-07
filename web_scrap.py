from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import json
from datetime import datetime

class HeavyWebsiteScraper:
    def __init__(self, headless=False,wait_time=10):
        print("starting the web scraper robot")
        self.wait_time = wait_time
        self.setup_browser(headless)
        self.scarped_data=[]
    def setup_browser(self,headless):
        print("settin gup chrome browser")
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            print("running invisible mode")
        else:
            print("running on visible mode")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
        chrome_options.add_experimental_option("'useAutomationExtension', False")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service,options=chrome_options)

        self.driver.execute
