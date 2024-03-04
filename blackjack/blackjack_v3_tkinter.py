import random
import os
import dataclasses
import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image

@dataclasses.dataclass
class Player:
    """
    Class created to streamline all the data
    that needs to be stored relating to the player and dealer.
    """
    hand: list = dataclasses.field(default_factory=list)
    hand_value: int = 0 # total hand value
    status: str = None # busted, blackjack, or stood
    is_player: bool = True # is used to find the winner


@dataclasses.dataclass
class State:
    """
    Main class to hold all variables that could be needed globally. 
    It's reset everytime a new game is started.
    """
    deck: list = dataclasses.field(default_factory=list)
    game_end: bool = False
    player: Player = dataclasses.field(default_factory=Player)
    dealer: Player = dataclasses.field(default_factory=lambda: Player(is_player=False))
    
class GUI:
    window = None
    state_label = None
    player_image_labels = {}
    dealer_image_labels = {}
    card_images = {}

def load_image(name):
    image_dir = os.path.join(IMAGE_PATH, name)
    print(image_dir)
    return ImageTk.PhotoImage(file=image_dir)

def label_maker(frame):
    return tk.Label(
        frame,
        text=" ",
        font=FONT,
        borderwidth=3,
        padx=20,
        pady=10,
        relief="groove",
    )


def btn_maker(state, frame, text):
    return tk.Button(frame, text=text, font=FONT, command=lambda: btn_op(state, text))


def update_label(label, text=None, color=None, image=None):
    label.configure(text=text, bg=color, image=image)


def create_deck(image_dir):
    """
    Input the directory of the image files then creates a
    list of all the cards with the card_back card removed.
    """
    full_deck = os.listdir(image_dir)
    full_deck.remove("card_back.png")
    return full_deck


def get_hand(state, player):
    """
    Takes in the state dataclass and the boolean
    of if it's for the player, then returns the
    hand for either dealer or player.
    """
    if player:
        hand = state.player.hand
    else:
        hand = state.dealer.hand
    return hand


def get_status(state, player):
    """
    Takes in the state dataclass and the boolean of
    if it's for the player, then returns the statys
    for either dealer or player.
    """
    if player:
        status = state.player.status
    else:
        status = state.dealer.status
    return status


def deal_card(state, player):
    """
    Uses pop to draw a card from the deck into the
    inputted player's hand.
    """
    hand = get_hand(state, player)
    card = state.deck.pop()
    if player:
        print(f"player drew {card}")
    else:
        print(f"dealer drew {card}")
    hand.append(card)
    display_hand(state, player)


def calculate_score(state, player):
    """
    Returns the total value of the dealer or player's hand.
    Also checks to see if players have busted or gotten a blackjack.
    """
    hand_value = 0
    aces = 0
    hand = get_hand(state, player)
    for card in hand:
        if card == "card_back.png":
            continue
        number, _, suit = card.split("_", 2)

        numeric = number.isnumeric()

        if numeric == True:
            value = int(number)
        elif number == "ace":
            value = 11
            aces += 1
        else:
            value = 10
        hand_value += value

    if hand_value == 21:
        if player:
            state.player.status = "blackjack"
        else:
            state.dealer.status = "blackjack"
    while aces > 0 and hand_value > 21:
        aces -= 1
        hand_value -= 10
    if hand_value > 21:
        if player:
            state.player.status = "busted"
        else:
            state.dealer.status = "busted"
    return hand_value


def display_hand(state, player):
    """
    Get all the cards in inputted player's hand and then
    combine the strings and print.
    """
    update_value(state, player)
    hand = get_hand(state, player)
    cards = ""
    for i, card in enumerate(hand):
        cards += f"{card} "
        GUI.card_images[card] = image = load_image(card)
        if player:
            label = GUI.player_image_labels[i]
        else:
            label = GUI.dealer_image_labels[i]
        label.grid(row=0, column=i)
        update_label(label, image=image)
        print(f"player = {player}, label = {label}, image = {image}")

    if hand == state.player.hand:
        print(f"Your hand ({state.player.value}): ")
    else:
        print(f"Dealer's hand ({state.dealer.value}): ")
    print(cards)


def update_value(state, player):
    """
    Calculates the total hand value for either inputted player.
    Also calculates if player got a blackjack or busted.
    """
    if player:
        state.player.value = calculate_score(state, player)
    else:
        state.dealer.value = calculate_score(state, player)


def game_setup(state, full_deck):
    """
    Runs before every game, it creates a new deck,
    shuffles it and deals the first cards to the player
    and dealer.
    """
    state.deck = deck = list(full_deck)
    random.shuffle(deck)
    state.player.hand = [deck.pop(), deck.pop()]
    state.dealer.hand = [deck.pop(), "card_back.png"]
    print("-" * 25)


def restart_game(state):
    """
    Takes input from the player if they
    want to continue playing if not, it stops
    the program.
    """
    restart = input("Do you want to stop playing (y)? If empty continue. ")
    if restart == "y":
        print("Thanks for playing.")
        raise SystemExit
    else:
        pass


def win_check(state, player):
    """
    Takes an input player and returns what the game outcome is,
    player won, dealer won, or tie.
    """
    winner = None
    status = get_status(state, player)

    if state.player.is_player == player:
        user = "player"
        opponent = "dealer"
    else:
        user = "dealer"
        opponent = "player"

    if status == "blackjack":
        if state.player.value == state.dealer.value:
            winner = "tie"
        else:
            winner = user

    if status == "busted":
        winner = opponent

    if state.player.status and state.dealer.status == "stood":
        if state.player.value > state.dealer.value:
            winner = "player"
        elif state.player.value < state.dealer.value:
            winner = "dealer"
        else:
            winner = "tie"

    return winner


def status_check(state, player):
    """
    Ends the game if end conditions are met,
    and prints both player's total hand value
    and the final winner.
    """
    update_value(state, player)
    winner = win_check(state, player)

    if winner == None:
        return
    
    state.game_end = True
    if "card_back.png" in state.dealer.hand:
        del state.dealer.hand[-1]
        deal_card(state, player=False)

    if winner == "tie":
        print(
            f"The game has ended in a tie, {state.player.value} to {state.dealer.value}"
        )
    else:
        print(
            f"{winner} wins, player had {state.player.value} to the dealer's {state.dealer.value}"
        )


    restart_game(state)

def dealer_turn(state):
    """
    After the player stands or gets blackjack
    the dealer plays. Reveals what the hidden card
    is before hitting until reaching a total hand
    value above or equal to 17.
    """
    del state.dealer.hand[-1]
    deal_card(state, player=False)

    while state.dealer.value < 17:
        deal_card(state, player=False)
        status_check(state, player=False)
        if state.game_end:
            return
    state.dealer.status = "stood"
    status_check(state, player=False)

def btn_op(state, text):
    """Updates the label for normal keyboard,
    or does specific function for special buttons."""
    if not state.game_end:
        if text == "Hit":
            deal_card(state, player=True)
            status_check(state, player=True)

        elif text == "Stand":
            state.player.status = "stood"
            #GUI.window.unbind("Hit")
            #GUI.window.unbind("Stand")

        elif text == "Reset":
            state = State()
            

def game(state, full_deck):
    print("Welcome to Blackjack!") # create a new instance to reset all variables
    game_setup(state, full_deck)
    display_hand(state, player=False)
    display_hand(state, player=True)
    status_check(state, player=False)
    status_check(state, player=True)
    #dealer_turn(state)
    #if state.game_end:
    #    continue

def main():
    global IMAGE_PATH
    global FONT
    
    GUI.window = window = tk.Tk()
    GUI.window.title("Blackjack")
    GUI.window.resizable(False, False)

    script_dir = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(script_dir, "best_cards")
    FONT = font.Font(family="Courier", size=30, weight="bold")
    full_deck = create_deck(IMAGE_PATH)

    state = State()

    dealer_frame = tk.Frame(window, width=300, height=30, bg="honeydew2")
    dealer_frame.grid(row=1, column=0)

    player_frame = tk.Frame(window, width=300, height=30, bg="honeydew2")
    player_frame.grid(row=2, column=0)

    button_frame = tk.Frame(window, width=300, height=10, bg="honeydew2")
    button_frame.grid(row=3, column=0)

    hit_button = btn_maker(state, button_frame, "Hit")
    hit_button.grid(row=0, column=0)
    stand_button = btn_maker(state, button_frame, "Stand")
    stand_button.grid(row=0, column=1)

    for i in range(11):
        GUI.player_image_labels[i] = (label_maker(player_frame))
        GUI.dealer_image_labels[i] = (label_maker(dealer_frame))
        print(f"creating label #{i}")
    print(f"player labels: {GUI.player_image_labels}")

    game(state, full_deck)

    window.mainloop()

if __name__ == "__main__":
    main()

