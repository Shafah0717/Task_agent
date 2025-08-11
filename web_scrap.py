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
import random
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

        self.driver.execute_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")

        self.wait = WebDriverWait(self.driver,self.wait_time)

    def human_delay(self,min_seconds=1,max_seconds=4):
        delay = random.uniform(min_seconds,max_seconds)
        print(f"Taking a human-like break for {delay:.1f} seconds")
        time.sleep(delay)
    def go_to_page(self,url):
        print(f"visting this site {url}")
        self.driver.get(url)
        self.human_delay(2,4)
        print("page loaded")
    
    def wait_for_elements(self,css_selector,timeout=None):
        if timeout is None:
            timeout = self.wait_time
        
        try:
            print(f"wait for element {css_selector}")
            element = WebDriverWait(self.driver,timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,css_selector))
            )
            print("element found")
            return element
        except:
            print(f"Element not found:{css_selector}")
            return None
    def scroll_page(self,scrolls=3,scroll_pause=2):
        print(f"scrolling page {scrolls},times")

        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            print(f"Scroll {i+1} completed")
            time.sleep(scroll_pause)
    
    def infinite_scroll(self,max_scroll=10):
        print("🔄 Starting infinite scroll...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        scrolls=0

        while scrolls < max_scroll:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.script.scrollHeight")
            if new_height == last_height:
                print("no more content to load ")
                break
            if new_height == last_height:
                print("No more content to load!")
                break
                
            last_height = new_height
            scrolls += 1
            print(f"Infinite scroll {scrolls}")
        
        print(f"Infinite scrolling done! Did {scrolls} scrolls")
    
    def click_element(self,css_selector):
        try:
            element = self.wait_for_elements(css_selector)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);",element)
                element.click()
                self.human_delay(1, 2)

                element.click()
                print(f"clicked: {css_selector}")
                self.human_delay(1,3)
                return True
            else:
                print(f"Could not find element to click: {css_selector}")
                return False
        except Exception as e:
            print(f"Error clicking {css_selector}: {e}")
            return False
    
    def type_text(self,css_selectors,text):
        try:
            element = self.wait_for_elements(css_selector)
            if element:
                element.clear()
                element.send_keys(text)
                print(f"typed '{text}' into {css_selectors}")
                self.human_delay(1,2)
                return True
        except Exception as e:
            print(f"error for typing into {css_selectors}: {e}")
            return False
