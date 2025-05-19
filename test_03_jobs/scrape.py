import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

BASE_URL = "https://remoteok.com/"
jobs = []

# Using Playwright to handle dynamic content
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE_URL)

    # Wait for jobs to load (optional but useful for dynamic content)
    page.wait_for_selector("tr.job")
    
    # Scroll to the bottom of the page to trigger lazy loading
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # Wait 3 seconds for additional jobs to load 
    page.wait_for_timeout(3000)
    
    # Extract job details
    html = page.content()
    soup = BeautifulSoup(html, 'lxml')

    browser.close()

# Check job listings 
jobss = soup.find_all("tr", class_="job")
print(f"Found {len(jobss)} jobs on the page.")

# Extract job listings
for listing in jobss:
    print("Scraping page...")
    jobTitle = listing.select_one(".company h2").text.strip()
    company = listing.select_one(".companyLink h3").text.strip()
    location = listing.select_one(".location").text.strip()
    link = listing.get("data-href", "").strip()
    
    
    jobs.append({
        "job_title": jobTitle,
        "company": company,
        "location": location,
        "link": BASE_URL + link
    })
    
df = pd.DataFrame(jobs)
df.to_csv("test_03_jobs\\output.csv", index=False)
print("Done! Saved to output.csv") 