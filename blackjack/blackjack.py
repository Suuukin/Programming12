import os
import random
import dataclasses


class State:
    cards = []
    current_deck = []
    player_hand = []
    player_value = 0
    house_hand = []
    house_value = 0


@dataclasses.dataclass
class Card:
    filename: str
    name: str
    suit: str
    value: int

    def get_image(self):
        raise NotImplementedError


def card_finder(image_dir):
    card_names = os.listdir(image_dir)
    for filename in card_names:

        if filename == "card_back.png":
            continue
        name, _, ext = filename.rpartition(".")
        number, _, suit = name.split("_", 2)

        numeric = number.isnumeric()

        if numeric == True:
            value = int(number)
        elif number == "ace":
            value = 11
        else:
            value = 10
        State.cards.append(Card(filename, name, suit, value))


def draw_card(player):
    card = random.choice(State.current_deck)
    if player == True:
        State.player_hand.append(card)
        State.player_value += card.value
    else:
        State.house_hand.append(card)
        State.house_value += card.value
    State.current_deck.remove(card)


def game_start():
    State.current_deck = list(State.cards)
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
    card_names = " ".join(c.name for c in State.player_hand)
    print(f"player hand is {card_names} and has a total value of {State.player_value}")


if __name__ == "__main__":
    main()
