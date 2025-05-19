import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://news.ycombinator.com/"
posts = []

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")

def parse_post(post):
    title = post.select_one(".titleline a").text
    link = post.select_one(".titleline a")["href"]
    
    subtext_row = post.find_next_sibling("tr")
    score_tag = subtext_row.select_one(".score")
    score = score_tag.text if score_tag else "0 points"
    
    
    posts.append({
        "title": title,
        "link": link,
        "score": score
    })
    
def scrape_posts(num_pages):
    url = BASE_URL
    
    for page in range(num_pages):
        print(f"Scraping page {page + 1}...")
        soup = get_soup(url)
        
        for item in soup.select("tr.athing.submission"):
            parse_post(item)
            
        next_page = soup.select_one("a.morelink")
        if next_page:
            next_href = next_page["href"]
            url = BASE_URL + next_href
        else:
            break
    
scrape_posts(3)
df = pd.DataFrame(posts)
df.to_csv("test_02_news\\output.csv", index=False)
print("Done! Saved to output.csv")
