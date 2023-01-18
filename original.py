# website used: https://quotes.toscrape.com/
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

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
    return all_quotes
    # sleep(2)


# ----- GAME ----

def game_logic(quotes):
    quote = choice(quotes)
    num_guesses = 4
    guess = ""
    print("Here's a quote: ")
    print(quote["text"])
    # print(quote["author"]) uncomment to see answer
    while guess.lower() != quote["author"].lower() and num_guesses > 0:
        guess = input(
            f"Who said this quote? Guesses remaining: {num_guesses} \n")
        num_guesses -= 1
        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT!")
            break
        elif num_guesses == 3:
            res = requests.get(f"{base_url}{quote['about-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                f"Here's a hint: The author was born on {birth_date} {birth_place}")
        elif num_guesses == 2:
            print(
                f"Another hint: The author's first name starts with the letter {quote['author'][0]}")
        elif num_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(
                f"Another hint: The author's last name starts with the letter {last_initial}")
        else:
            print(
                f"Sorry, you ran out of guesses! The answer was {quote['author']} ")

    again = ""
    while again not in ("y", "yes", "n", "no"):
        again = input("Would you like to play again (y/n)? \n")

        if again.lower() in ("yes", "y"):
            return game_logic(quotes)
        else:
            print("Ok, Game is Over :-)")


quotes = quotes_scraping()
game_logic(quotes)
