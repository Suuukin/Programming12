import os
import random

def card_finder(image_dir):
    cards = {}  
    card_names = os.listdir(image_dir)

    for card in card_names:

        if card == "card_back.png":
            continue
        
        number, placeholder, suit = card.split("_")
        numeric = number.isnumeric()

        if numeric == True:
            card_value = number
        elif number == "ace":
            card_value = 11
        else:
            card_value = 10
        cards[card] = card_value

    return cards


def main():
    script_dir = os.path.dirname(__file__)
    image_dir = os.path.join(script_dir, "best_cards")

    cards = card_finder(image_dir)
    card, card_value = random.choice(list(cards.items())) 
    print(card, card_value)
if __name__ == "__main__":
    main()