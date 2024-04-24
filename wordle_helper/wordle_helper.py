import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as font
import wordlist
import collections

# This is a modified version of the original template Mr. Poy
# created. This version is for displaying a list of words
# that meets the criteria of the app.state you are playing

window = tk.Tk()
window.title("Wordle Cheater")
window.resizable(False, False)

large_font = font.Font(family="Courier", size=40, weight="bold")
small_font = font.Font(family="Courier", size=20, weight="bold")


class Char:
    # Class tracks the qualities of the guess buttons.
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.character = " "
        self.color = "grey"


class Row:
    # Class representing each guess row.
    def __init__(self, row_number):
        self.row = row_number
        self.guess = ""
        self.letter_count = 0

    def delete_char(self, char_dict):
        # Removes the last letter in current row
        if self.letter_count != 0:
            x = self.letter_count - 1
            y = self.row
            self.letter_count -= 1
            self.guess = self.guess[:-1]
            char_dict[(x, y)].character = " "
            char_dict[(x, y)].color = "grey"
            guess_buttons[(x, y)]["text"] = " "
            guess_buttons[(x, y)]["bg"] = "grey"

    def add_char(self, letter, char_dict):
        # Adds character to the button with position (x, y)
        if self.letter_count < 5:
            (x, y) = (self.letter_count, self.row)
            char_dict[(x, y)].character = letter
            guess_buttons[(x, y)]["text"] = letter
            self.guess += letter
            self.letter_count += 1


class State:
    """Class holds all variables and objects that need to be reset."""

    def __init__(self):
        self.current_row = 0
        self.guess_rows = {}
        self.char_dict = {}

        for x in range(5):
            for y in range(6):
                self.char_dict[(x, y)] = Char(x, y)

        for row in range(6):
            self.guess_rows[row] = Row(row)

    def do_delete_char(self):
        self.guess_rows[self.current_row].delete_char(self.char_dict)

    def btn_click(self, letter):
        self.guess_rows[self.current_row].add_char(letter, self.char_dict)


class App:
    """Main class, holds things that persist."""

    def __init__(self):
        self.word_list = set(wordlist.wordle_list)
        self.state = State()

    def btn_click(self, letter):
        self.state.btn_click(letter)

    def do_delete_char(self):
        self.state.do_delete_char()


app = App()


def create_button(letter, frame=window):
    new_button = tk.Button(
        frame,
        text=letter,
        bg="grey",
        fg="black",
        font=small_font,
        command=lambda: app.btn_click(letter)
    )
    return new_button


def color_label(button_position):
    # changes the color of the clicked button
    button = guess_buttons[button_position]
    background_color = app.state.char_dict[button_position].color
    if background_color == "grey":
        button["bg"] = "yellow"
        app.state.char_dict[button_position].color = "yellow"
    elif background_color == "yellow":
        button["bg"] = "green"
        app.state.char_dict[button_position].color = "green"
    elif background_color == "green":
        button["bg"] = "grey"
        app.state.char_dict[button_position].color = "grey"


def letter_check(letter_color, letter, word, letter_position, green_letters):
    """
    returns if the input word is a possible guess,
    based off the positions of it's letters and colors.
    """
    if letter_color == "grey":
        if letter not in word or letter in green_letters:
            return True
    elif letter_color == "yellow":
        if letter in word and word[letter_position] != letter:
            return True
    elif letter_color == "green":
        if word[letter_position] == letter:
            return True
    return False


def count_letters(possible_words, green_letters):
    """
    Returns a Counter object that has the frequency of all letters
    in the remaining possible guesses. Only counts the first
    appearance of each letter in a word.
    """
    letter_counter = collections.Counter()
    for word in possible_words:
        for c in set(word):
            letter_counter[c] += 1
    for letter in green_letters:
        del letter_counter[letter]
    return letter_counter


def evaluate_guesses(letter_count, word_list):
    """
    Returns a list of input words sorted in descending order
    based on their score.
    Scores words based on the frequency of the letters they contain.
    Gives no points for green letters, and gives no points for words
    with letters that are known to be yellow in their position.
    """

    def word_score(word):
        word_score = 0

        for c in set(word):
            letter_score = letter_count[c]

            for pos, slot in app.state.char_dict.items():
                x, y = pos
                if slot.character == word[x] and slot.color == "yellow":
                    letter_score = 0

            word_score += letter_score

        return word_score

    sorted_words = sorted(word_list, reverse=True, key=word_score)
    return sorted_words[:5]


def find_possible_words():
    """
    Takes all input guesses and colors then
    fills text_area with possible guesses, suggested guesses from all words,
    and suggested guesses from remaining words.
    """
    text_area.configure(state="normal")
    green_letters = []
    excluded_words = set()
    for row, guess_row in app.state.guess_rows.items():
        for column, letter in enumerate(guess_row.guess):
            letter_color = app.state.char_dict[(column, row)].color
            if letter_color == "green":
                if letter not in green_letters:
                    green_letters.append(letter)

            for word in app.word_list - excluded_words:
                keep_word = letter_check(
                    letter_color, letter, word, column, green_letters
                )

                if not keep_word:
                    excluded_words.add(word)

    letter_counter = count_letters((app.word_list - excluded_words), green_letters)
    suggested_guesses = evaluate_guesses(letter_counter, app.word_list)
    possible_guesses = evaluate_guesses(
        letter_counter, (app.word_list - excluded_words)
    )

    suggested_string = ", ".join(suggested_guesses)
    possible_string = ", ".join(possible_guesses)

    guess_string = f"Suggested Guesses: {suggested_string} \n\nGuesses from Possible Words: {possible_string} \n\n"

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, guess_string)
    text_area.insert(tk.END, sorted(app.word_list - excluded_words))
    text_area.configure(state="disabled")
    if app.state.current_row < 5:
        app.state.current_row += 1


def full_reset():
    """
    Makes a new copy of State() and clears text area and guess buttons.
    """
    app.state = State()
    for i in guess_buttons:
        guess_buttons[i].configure(text=" ", bg="grey")
    text_area.configure(state="normal")
    text_area.delete("1.0", tk.END)
    text_area.configure(state="disabled")


guess_frame = tk.Frame(window)
guess_frame.pack(side=tk.TOP)

keyboard_frame = tk.Frame(window)
keyboard_frame.pack(side=tk.TOP)

potential_words_frame = tk.Frame(window)
potential_words_frame.pack(side=tk.TOP)

guess_buttons = {}
# creates a 5x6 grid of buttons that act as labels.
for y in range(6):
    for x in range(5):
        guess_buttons[(x, y)] = button = tk.Button(
            guess_frame,
            text=" ",
            bg="grey",
            fg="black",
            font=small_font,
            command=lambda pos=(x, y): color_label(pos),
        )
        # place the label at an x,y position
        button.grid(row=y, column=x)

# Creates a keyboard based on the rows of keys on QWERTY keyboard.
# Stores the created buttons in a dictionary based on their string.
KEY_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
keyboard_frames = {}
for row, key_row in enumerate(KEY_ROWS):
    keyboard_frames[row] = frame = tk.Frame(
        keyboard_frame, width=300, height=50, bg="honeydew2"
    )
    frame.grid(row=row, column=1)
    keys = list(key_row)
    for column, key_text in enumerate(keys):
        keyboard_frames[key_text] = button = create_button(key_text, frame=frame)
        window.bind(str(key_text), lambda event, k=key_text: app.btn_click(k))
        button.grid(row=1, column=column + 1)

del_button = tk.Button(
    keyboard_frames[1],
    text="DEL",
    bg="grey",
    fg="black",
    font=small_font,
    command=app.do_delete_char,
)
del_button.grid(row=1, column=12)
window.bind(
    "<BackSpace>",
    lambda event: app.do_delete_char(),
)

enter_button = tk.Button(
    keyboard_frames[2],
    text="ENTR",
    bg="grey",
    fg="black",
    font=small_font,
    command=find_possible_words,
)
enter_button.grid(row=1, column=10)
window.bind("<Return>", lambda event: find_possible_words())

text_area = scrolledtext.ScrolledText(
    potential_words_frame, wrap=tk.WORD, width=50, height=20, state="disabled"
)
text_area.grid(row=0, column=0, sticky="nsew")

reset_button = tk.Button(
    potential_words_frame,
    text="Reset",
    bg="grey",
    fg="black",
    font=small_font,
    command=lambda: full_reset(),
)
reset_button.grid(row=1, column=0)

window.mainloop()
