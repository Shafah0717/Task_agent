import requests
from bs4 import BeautifulSoup

def get_website_title(url):
    print(f"Getting website: {url}")
    response = requests.get(url)
    if response.status_code==200:
        print("website responded successfully")
    else:
        print("website didnt respond quickly")
        return None
    soup = BeautifulSoup(response.content,'html.parser')
    title=soup.find('title')
    if title:
        return title.text.strip()
    else:
        return "no title found"
website_url = "https://www.wikipedia.org"
title = get_website_title(website_url)
print(f"The title is: {title}")