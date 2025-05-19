import requests
import pandas as pd

base_url = "https://quotes.toscrape.com/api/quotes?page="
page = 1
all_quotes = []

while True:
    response = requests.get(base_url + str(page))
    data = response.json()

    for quote in data["quotes"]:
        all_quotes.append({
            "text": quote["text"],
            "author": quote["author"]["name"],
            "tags": ", ".join(quote["tags"])
        })

    if not data["has_next"]:
        break
    page += 1

# Export to CSV
df = pd.DataFrame(all_quotes)
df.to_csv("quotes_api_output.csv", index=False)
df.to_csv("test_04_quotes_(api)\\output(api).csv", index=False)
print(f"Scraped {len(df)} quotes. Saved to quotes_api_output.csv.")
