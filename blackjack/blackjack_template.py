import random
import os

def create_deck():
    deck = os.listdir()
    deck.remove ('blackjack.py')
    deck.remove ('card_back.png')
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    #add your code here
    pass

def display_hand(hand):
    if len(hand) == 1:
        card = (hand[0])
        print (card)
        print ('card_back.png')
    else:
        for card in hand:
            print(card)
    

def game():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop()]

    print("Welcome to Blackjack!")
    print("Your hand:")
    display_hand(player_hand)
    print("Dealer's hand:")
    display_hand(dealer_hand)

game()
