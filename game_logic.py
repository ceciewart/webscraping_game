import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader
# ----- GAME ----
base_url = "https://quotes.toscrape.com/"


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def game_logic(quotes):
    quote = choice(quotes)
    num_guesses = 4

    print("Here's a quote: ")
    print(quote["text"])
    print(quote["author"])
    guess = ""
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

    again = " "
    while again not in ("y", "yes", "n", "no"):
        again = input("Would you like to play again (y/n)? \n")

        if again.lower() in ("yes", "y"):
            return game_logic()
        else:
            print("Ok, Game is Over :-)")


quotes = read_quotes("quotes.csv")

game_logic(quotes)
