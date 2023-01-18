# website used: https://quotes.toscrape.com/
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter
# ---- SCRAPING QUOTES AND SAVING THEM ----


base_url = "https://quotes.toscrape.com/"


def quotes_scraping():
    all_quotes = []  # where all quotes from the website get stored
    url = "/page/1"
    while url:
        res = requests.get(f"{base_url}{url}")
        print(f"Now Scraping {base_url}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

# A loop to grab all quotes and author names and create a dictionary of each, which is appended to the all_quotes list.
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "about-link": quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(1)
    return all_quotes

# Writing quotes to a csv file:


def quotes_writing(quotes):
    with open("quotes.csv", "w") as file:
        headers = ["text", "author", "about-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()

        for quote in quotes:
            csv_writer.writerow(quote)


quotes = quotes_scraping()
quotes_writing(quotes)
