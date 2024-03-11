import random
import os
import dataclasses
import tkinter as tk
import tkinter.font as Font
from PIL import ImageTk, Image

# flake8: noqa


@dataclasses.dataclass
class Player:
    """
    Class created to streamline all the data
    that needs to be stored relating to the player and dealer.
    """

    hand: list = dataclasses.field(default_factory=list)
    hand_value: int = 0  # total hand value
    status: str = None  # busted, blackjack, or stood
    is_player: bool = True  # is used to find the winner


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


class App:
    def __init__(self):
        self.state = State()
        self.game_state_label = None
        self.player_value_label = None
        self.dealer_value_label = None
        self.player_image_labels = {}
        self.dealer_image_labels = {}
        self.card_images = {}
        self.card_cropped = {}
        self.full_deck = []
        self.player_wins = 0
        self.dealer_wins = 0
        self.window_resized = False


def load_image(app, name):
    image_dir = os.path.join(app.image_path, name)
    image = Image.open(image_dir).convert("RGBA")
    return image


def label_maker(app, frame=None, text=" "):
    return tk.Label(
        frame,
        text=text,
        font=app.font,
        borderwidth=3,
        padx=20,
        pady=10,
        relief="groove",
    )


def btn_maker(app, frame, text):
    return tk.Button(frame, text=text, font=app.font, command=lambda: btn_op(app, text))


def update_label(label, text=None, color=None, image=None, font=None):
    label.configure(text=text, bg=color, image=image, font=font)


def create_deck(image_dir):
    """
    Input the directory of the image files then creates a
    list of all the cards with the card_back card removed.
    """
    full_deck = os.listdir(image_dir)
    full_deck.remove("card_back.png")
    return full_deck


def get_hand(app, player):
    """
    Takes in the app.state dataclass and the boolean
    of if it's for the player, then returns the
    hand for either dealer or player.
    """
    if player:
        hand = app.state.player.hand
    else:
        hand = app.state.dealer.hand
    return hand


def get_status(app, player):
    """
    Takes in the app.state dataclass and the boolean of
    if it's for the player, then returns the statys
    for either dealer or player.
    """
    if player:
        status = app.state.player.status
    else:
        status = app.state.dealer.status
    return status


def calculate_score(app, player):
    """
    Returns the total value of the dealer or player's hand.
    Also checks to see if players have busted or gotten a blackjack.
    """
    hand_value = 0
    aces = 0
    hand = get_hand(app, player)
    for card in hand:
        if card == "card_back.png":
            continue
        number, _, suit = card.split("_", 2)

        numeric = number.isnumeric()

        if number == "ace":
            value = 11
            aces += 1
        elif numeric:
            value = int(number)
        else:
            value = 10
        hand_value += value

    if hand_value == 21:
        if player:
            app.state.player.status = "blackjack"
        else:
            app.state.dealer.status = "blackjack"
    while aces > 0 and hand_value > 21:
        aces -= 1
        hand_value -= 10
    if hand_value > 21:
        if player:
            app.state.player.status = "busted"
        else:
            app.state.dealer.status = "busted"
    return hand_value


def shrink_check(app, hand):
    window_width = app.window.winfo_width()
    card_width = 125
    card_spaces = (window_width - 40) / card_width
    card_stack = False

    if card_spaces < len(hand):
        card_stack = True

    if window_width < 600:
        update_label(app.game_state_label, font=app.small_font)
        app.hit_button.configure(font=app.small_font)
        app.stand_button.configure(font=app.small_font)
        app.reset_button.configure(font=app.small_font)
    else:
        update_label(app.game_state_label, font=app.font)
        app.hit_button.configure(font=app.font)
        app.stand_button.configure(font=app.font)
        app.reset_button.configure(font=app.font)
    return card_stack


def display_hand(app, player):
    """
    Get all the cards in inputted player's hand and then
    combine the strings and print.
    """
    update_value(app, player)
    hand = get_hand(app, player)
    cards = ""

    card_stack = shrink_check(app, hand)

    for i, card in enumerate(hand):
        cards += f"{card} "

        if card not in app.card_images.keys():
            img = load_image(app, card)

            app.card_images[card] = ImageTk.PhotoImage(img)

            width, height = img.size

            img2 = img.crop([0, 0, width / 4, height])
            app.card_cropped[card] = ImageTk.PhotoImage(img2)

        if player:
            label = app.player_image_labels[i]
        else:
            label = app.dealer_image_labels[i]

        if card_stack and i != len(hand) - 1:
            image = app.card_cropped[card]
        else:
            image = app.card_images[card]

        label.grid(row=0, column=i)
        update_label(label, image=image)

    if hand == app.state.player.hand:
        label = app.player_value_label
        value = app.state.player.hand_value
    else:
        label = app.dealer_value_label
        value = app.state.dealer.hand_value
    update_label(label, text=value)


def update_value(app, player):
    """
    Calculates the total hand value for either inputted player.
    Also calculates if player got a blackjack or busted.
    """
    if player:
        app.state.player.hand_value = calculate_score(app, player)
    else:
        app.state.dealer.hand_value = calculate_score(app, player)


def deal_card(app, player):
    """
    Uses pop to draw a card from the deck into the
    inputted player's hand.
    """
    hand = get_hand(app, player)
    card = app.state.deck.pop()
    hand.append(card)
    display_hand(app, player)


def clear_hide_label(label):
    update_label(label, image=None)
    label.grid_remove()


def win_check(app, player):
    """
    Takes an input player and returns what the game outcome is,
    player won, dealer won, or tie.
    """
    winner = None
    status = get_status(app, player)

    player_value = app.state.player.hand_value
    dealer_value = app.state.dealer.hand_value

    if app.state.player.is_player == player:
        user = "player"
        opponent = "dealer"
    else:
        user = "dealer"
        opponent = "player"

    if status == "blackjack":
        if player_value == dealer_value:
            winner = "tie"
        else:
            winner = user

    if status == "busted":
        winner = opponent

    if app.state.player.status and app.state.dealer.status == "stood":
        if player_value > dealer_value:
            winner = "player"
        elif player_value < dealer_value:
            winner = "dealer"
        else:
            winner = "tie"

    if winner == "player":
        app.player_wins += 1
    elif winner == "dealer":
        app.dealer_wins += 1
    return winner


def status_check(app, player):
    """
    Ends the game if end conditions are met,
    and prints both player's total hand value
    and the final winner.
    """
    update_value(app, player)
    winner = win_check(app, player)
    if winner:
        app.state.game_end = True

        if "card_back.png" in app.state.dealer.hand:
            del app.state.dealer.hand[-1]
            deal_card(app, player=False)

        if winner == "tie":
            string = f"Tie, P:{app.state.player.hand_value} to D:{app.state.dealer.hand_value}"
        else:
            winner = winner.capitalize()
            string = f"{winner} wins, P:{app.state.player.hand_value} to D:{app.state.dealer.hand_value}"
        update_label(app.game_state_label, text=string)


def dealer_turn(app):
    """
    After the player stands or gets blackjack
    the dealer plays. Reveals what the hidden card
    is before hitting until reaching a total hand
    value above or equal to 17.
    """
    del app.state.dealer.hand[-1]
    deal_card(app, player=False)

    while app.state.dealer.hand_value < 17:
        deal_card(app, player=False)
        status_check(app, player=False)
        if app.state.game_end:
            return
    app.state.dealer.status = "stood"
    status_check(app, player=False)


def player_stand(app):
    app.state.player.status = "stood"
    dealer_turn(app)


def btn_op(app, text):
    """Updates the label for normal keyboard,
    or does specific function for special buttons."""
    if text == "Reset":
        game(app)
        update_label(
            app.game_state_label,
            f"Player to Dealer wins {app.player_wins}:{app.dealer_wins}",
        )
    if not app.state.game_end:
        if text == "Hit":
            deal_card(app, player=True)
            status_check(app, player=True)

        elif text == "Stand":
            player_stand(app)


def window_resized(event):
    window_resized = True
    return window_resized


def resizer(app):
    if app.window_resized:
        display_hand(app, player=False)
        display_hand(app, player=True)
        app.window_resized == False
    app.window.after(200, resizer, app)


def game(app):
    app.window_resized == True

    for i in range(len(app.player_image_labels)):
        clear_hide_label(app.player_image_labels[i])
        clear_hide_label(app.dealer_image_labels[i])

    app.state = State()
    app.state.deck = deck = list(app.full_deck)

    random.shuffle(deck)

    app.state.player.hand = [deck.pop(), deck.pop()]
    app.state.dealer.hand = [deck.pop(), "card_back.png"]

    status_check(app, player=False)
    status_check(app, player=True)


def main():
    app = App()

    app.window = window = tk.Tk()
    window.title("Blackjack")
    window.configure(bg="green")
    window.geometry("900x750")

    script_dir = os.path.dirname(__file__)
    app.image_path = image_path = os.path.join(script_dir, "best_cards")
    app.font = font = Font.Font(family="Courier", size=30, weight="bold")
    app.small_font = Font.Font(family="Courier", size=15, weight="bold")
    app.full_deck = create_deck(image_path)

    app.game_state_label = label_maker(app, text="Welcome to Blackjack!")
    app.game_state_label.pack(side=tk.TOP, fill="x")

    spacer1 = tk.Label(window, bg="Green")
    spacer1.pack(side=tk.TOP, expand=True, fill="y")

    dealer_frame = tk.Frame(window, width=300, height=30, bg="Green")
    dealer_frame.pack(side=tk.TOP)

    app.dealer_value_label = label_maker(app, text=app.state.dealer.hand_value)
    app.dealer_value_label.pack(side=tk.TOP)

    spacer2 = tk.Label(window, bg="Green")
    spacer2.pack(side=tk.TOP, expand=True, fill="y")

    player_frame = tk.Frame(window, width=300, height=30, bg="Green")
    player_frame.pack(side=tk.TOP)

    app.player_value_label = label_maker(app, text=app.state.player.hand_value)
    app.player_value_label.pack(side=tk.TOP)

    spacer3 = tk.Label(window, bg="Green")
    spacer3.pack(side=tk.TOP, expand=True, fill="y")

    button_frame = tk.Frame(window, width=300, height=10, bg="Green")
    button_frame.pack(side=tk.TOP)

    app.hit_button = btn_maker(app, button_frame, "Hit")
    app.hit_button.grid(row=0, column=0)
    app.stand_button = btn_maker(app, button_frame, "Stand")
    app.stand_button.grid(row=0, column=1)
    app.reset_button = btn_maker(app, button_frame, "Reset")
    app.reset_button.grid(row=0, column=2)

    for i in range(11):
        app.player_image_labels[i] = label_maker(app, player_frame)
        app.dealer_image_labels[i] = label_maker(app, dealer_frame)

    app.window_resized = app.game_state_label.bind("<Configure>", window_resized)
    window.after(20, resizer, app)

    game(app)

    window.mainloop()


if __name__ == "__main__":
    main()
