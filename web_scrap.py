import requests
from bs4 import BeautifulSoup

def get_all_links(url):
    print(f"Getting website: {url}")
    response = requests.get(url)
    if response.status_code==200:
        print("website responded successfully")
    else:
        print("website didnt respond quickly")
        return None
    soup = BeautifulSoup(response.content,'html.parser')
    link_tags = soup.find_all('a')
    links=[]
    for link_tag in link_tags:
        href = link_tag.get('href')

        text = link_tag.text.strip()
        href_text = href.replace('//', '')
        if href and text:
            links.append({
                'text':text,
                'url':href_text
            })
    return links
website_url = "https://www.wikipedia.org"
all_links = get_all_links(website_url)

print("First 5 links found:")
for i, link in enumerate(all_links[:5]):
    print(f"{i+1}. {link['text']} -> {link['url']}")