import os
import random

class State:
    cards = {}
    deck = {}
    player_hand = {}
    player_value = 0
    house_hand = {}
    house_value = 0

def card_finder(image_dir):
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
        State.cards[card] = card_value

def draw_card(player):
    card = random.choice(list(State.cards.keys())) 
    card_value = State.cards[card]
    if player == True:
        State.player_hand[card] = card_value
        State.player_value += int(card_value)
    else:
        State.house_hand[card] = card_value
        State.house_value += int(card_value)
    del State.cards[card]

def game_start():
    draw_card(True)
    draw_card(True)
    draw_card(False)
    draw_card(False)
    return

def main():
    script_dir = os.path.dirname(__file__)
    image_dir = os.path.join(script_dir, "best_cards")
    card_finder(image_dir)
    game_start()
    print(f"player hand is {State.player_hand}, and a total value of {State.player_value}")

if __name__ == "__main__":
    main()