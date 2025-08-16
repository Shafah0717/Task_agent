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
            element = self.wait_for_elements(css_selectors)
            if element:
                element.clear()
                element.send_keys(text)
                print(f"typed '{text}' into {css_selectors}")
                self.human_delay(1,2)
                return True
        except Exception as e:
            print(f"error for typing into {css_selectors}: {e}")
            return False
    def extract_data(self, selectors_dict):
        print("🔍 Extracting data from current page...")
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {}
        
        for field_name, css_selector in selectors_dict.items():
            try:
                elements = soup.select(css_selector)
                
                if not elements:
                    data[field_name] = "NOT FOUND"
                elif len(elements) == 1:
                    data[field_name] = elements[0].get_text(strip=True)
                else:
                    data[field_name] = [elem.get_text(strip=True) for elem in elements]
                
                print(f"   ✅ {field_name}: Found {len(elements) if elements else 0} items")
                
            except Exception as e:
                print(f"   ❌ Error extracting {field_name}: {e}")
                data[field_name] = "ERROR"
        
        data['url'] = self.driver.current_url
        data['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return data
    
    def handle_popups(self,popup_close_selectors):
        print("checing for pop up")
        for selector in popup_close_selectors:
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                if close_button.is_displayed():
                    close_button.click()
                    print(f"  Closed popup using: {selector}")
                    self.human_delay(1, 2)
                    break
            except:
                continue
        print(" Popup check complete")

    def scrape_multiple_pages(self, urls,selectors , action_per_page=None):
        all_data=[]
        for i,url in enumerate(urls,1):
            print(f"\nSCRAPING PAGE {i}/{len(urls)}")
            print("=" * 50)
            self.go_to_page(url)

            if action_per_page:
                for action in action_per_page:
                    try:
                        action(self)
                    except Exception as e:
                        print(f"action failed {e}")
            data = self.extract_data(selectors)
            all_data.append(data)

            print(f"page {i} complete")

            if i <len(urls):
                self.human_delay(2,5)
        return all_data
    
    def save_data(self, data, filename=None):

        if not data:
            print(" No data to save!")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"scraped_data_{timestamp}"
        
        
        df = pd.json_normalize(data)  
        csv_file = f"{filename}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f" Saved {len(data)} records to {csv_file}")

        json_file = f"{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" Also saved to {json_file}")

    def close_browser(self):
        print(" Closing browser...")
        self.driver.quit()
        print(" Browser closed!")