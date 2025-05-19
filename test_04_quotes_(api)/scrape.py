import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://quotes.toscrape.com/"
quotes = []

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")

def parse_quote(quote):
    text = quote.select_one(".text").text
    auth = quote.select_one(".author").text
    
    quotes.append({
        "quote": text,
        "author": auth
    })
    
def scrape_posts(num_pages):
    url = BASE_URL
    
    for page in range(num_pages):
        print(f"Scraping page {page + 1}...")
        soup = get_soup(url)
        
        for item in soup.select("div.quote"):
            parse_quote(item)
            
        next_page = soup.select_one(".next > a")
        if next_page:
            next_href = next_page['href']
            url = BASE_URL + next_href
        else:
            break
    
scrape_posts(10)
df = pd.DataFrame(quotes)
df.to_csv("test_04_quotes_(api)\\output.csv", index=False)
print("Done! Saved to output.csv")
