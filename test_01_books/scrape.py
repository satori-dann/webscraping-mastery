import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
books = []

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")

def parse_book(book, base_url):
    title = book.h3.a["title"]
    product_url = urljoin(base_url, book.h3.a["href"])
    price = book.find("p", class_="price_color").text.strip()
    availability = book.find("p", class_="instock availability").text.strip()
    rating = book.p["class"][1]  # e.g., 'Three'
    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "url": product_url
    }

def scrape_all_books():
    page_url = BASE_URL + "catalogue/page-1.html"
    
    while True:
        print(f"Scraping {page_url}...")
        soup = get_soup(page_url)
        book_elements = soup.find_all("article", class_="product_pod")
        
        for book in book_elements:
            books.append(parse_book(book, BASE_URL + "catalogue/"))

        # Find "next" button
        next_btn = soup.find("li", class_="next")
        if not next_btn:
            break
        next_url = next_btn.a["href"]
        page_url = urljoin(page_url, next_url)

scrape_all_books()
df = pd.DataFrame(books)
df.to_csv("test_01_books\\output.csv", index=False)
print("Done! Saved to output.csv")
