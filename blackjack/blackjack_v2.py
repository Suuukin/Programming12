import random
import os
import dataclasses

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
    full_deck: list = dataclasses.field(default_factory=list)
    deck: list = dataclasses.field(default_factory=list)
    game_end: bool = False
    player: Player = dataclasses.field(default_factory=Player)
    dealer: Player = dataclasses.field(default_factory=lambda: Player(is_player=False))


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
    for card in hand:
        cards += f"{card} "
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


def player_turn(state):
    """
    Takes input from the player if they want to
    hit or to stand. As long as the player
    keeps hitting and they don't bust it will
    keep asking. If player does not want to hit
    they will stand and move on to dealer's turn.
    """
    while not state.game_end:
        hit_stand = input(
            f"Do you want to hit (y) otherwise stand? = {state.player.value}? "
        )
        if hit_stand == "y":
            deal_card(state, player=True)
            status_check(state, player=True)
        else:
            state.player.status = "stood"
            break


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


def game():
    script_dir = os.path.dirname(__file__)
    image_dir = os.path.join(script_dir, "best_cards")
    full_deck = create_deck(image_dir)
    print("Welcome to Blackjack!")
    while True:
        state = State() # create a new instance to reset all variables
        game_setup(state, full_deck)
        display_hand(state, player=False)
        display_hand(state, player=True)
        status_check(state, player=False)
        status_check(state, player=True)
        if state.game_end:
            continue
        player_turn(state)
        if state.game_end:
            continue
        dealer_turn(state)
        if state.game_end:
            continue


game()
