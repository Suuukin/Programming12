import random
import os

class State:
    deck = []
    player_hand = []
    dealer_hand = []

def create_deck(image_dir):
    deck = os.listdir(image_dir)
    deck.remove('card_back.png')
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    hand_value = 0
    for card in hand:
        name, _, ext = card.rpartition(".")
        number, _, suit = name.split("_", 2)

        numeric = number.isnumeric()

        if numeric == True:
            value = int(number)
        elif number == "ace":
            value = 11
        else:
            value = 10
        hand_value += value
    return hand_value
        

def display_hand(hand):
    hand_value = calculate_score(hand)
    if hand_value == 21:
        if hand == "dealer_hand":
            dealer_21 = True
        else:
            player_21 = True
    else:
        if hand == "dealer_hand":
            hidden_card = hand[0]
            del hand[0]
    for card in hand:
        print(card)
    
def game_setup(image_dir):
    full_deck = create_deck(image_dir)
    deck = list(full_deck)
    State.player_hand = [deck.pop(), deck.pop()]
    State.dealer_hand = [deck.pop(), deck.pop(), "card_back.png"]

def game():
    script_dir = os.path.dirname(__file__)
    image_dir = os.path.join(script_dir, "best_cards")
    game_setup(image_dir)
    print("Welcome to Blackjack!")
    print("Your hand:")
    display_hand(State.player_hand)
    print("Dealer's hand:")
    display_hand(State.dealer_hand)

game()
