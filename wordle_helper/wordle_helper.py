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
super_small_font = font.Font(family="Courier", size=20, weight="bold")


class Row:
    def __init__(self, row_number):
        self.row = row_number
        self.guess = ""
        self.result = None
        self.letter_count = 0

    def delete_char(self):
        if self.letter_count != 0:
            self.letter_count -= 1
            self.guess = self.guess[:-1]
            guess_buttons[(self.letter_count, self.row)]["text"] = " "
            guess_buttons[(self.letter_count, self.row)]["bg"] = "grey"


class State:
    def __init__(self):
        self.current_row = 1
        self.guess_rows = {}
        for row in range(1, 6):
            self.guess_rows[row] = Row(row)


class App:
    def __init__(self):
        self.word_list = set(wordlist.wordle_list)
        self.state = State()


app = App()


def create_label(frame=window):
    # Create a Tkinter Label
    new_label = tk.Label(
        frame,
        text=" ",
        bg="grey",
        fg="black",
        font=large_font,
        borderwidth=2,
        relief="solid",
    )
    return new_label


def create_button(letter, frame=window):
    # Create a Tkinter Label
    new_button = tk.Button(
        frame,
        text=letter,
        bg="grey",
        fg="black",
        font=small_font,
        command=lambda: btn_click(letter),
    )
    return new_button


def btn_click(letter):
    if app.state.letter_count_row["current_row"] < 5:
        guess_buttons[app.state.letter_count]["text"] = letter
        app.state.guess_rows[app.state.current_row] += letter
        app.state.letter_count += 1


def color_label(button_position):
    button = guess_buttons[button_position]
    background_color = button["bg"]
    if background_color == "grey":
        button["bg"] = "yellow"
    elif background_color == "yellow":
        button["bg"] = "green"
    elif background_color == "green":
        button["bg"] = "grey"


def letter_check(letter_color, letter, word, letter_position, green_letters):
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
    letter_counter = collections.Counter()
    for word in possible_words:
        for c in set(word):
            letter_counter[c] += 1
    for letter in green_letters:
        del letter_counter[letter]
    print(letter_counter)
    return letter_counter


def evaluate_guesses(letter_counter):

    def word_score(word):
        word_score = 0
        letters = set(word)
        for c in letters:
            word_score += letter_counter[c]
        return word_score

    sorted_words = sorted(app.word_list, reverse=True, key=word_score)

    return sorted_words[:10]


def find_possible_words():
    text_area.configure(state="normal")
    green_letters = []
    excluded_words = set()
    for i, letter in enumerate(app.state.guess):
        letter_color = guess_buttons[i]["bg"]
        if letter_color == "green":
            if letter not in green_letters:
                green_letters.append(letter)

        for word in app.word_list - excluded_words:
            keep_word = letter_check(letter_color, letter, word, i, green_letters)

            if not keep_word:
                excluded_words.add(word)

    letter_counter = count_letters((app.word_list - excluded_words), green_letters)

    sorted_scores = evaluate_guesses(letter_counter)
    print(sorted_scores)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, sorted(app.word_list - excluded_words))
    text_area.configure(state="disabled")


def full_reset():
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
for y in range(0, 6):
    for x in range(0, 5):
        guess_buttons[(x, y)] = button = tk.Button(
            guess_frame,
            text=" ",
            bg="grey",
            fg="black",
            font=super_small_font,
            command=lambda pos=(x, y): color_label(pos),
        )
        # place the label at an x,y position
        button.grid(row=y, column=x)

# Create a keyboard
# start with an empty dictionary called button = {}, then add elements button[1] etc
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
        window.bind(str(key_text), lambda event, k=key_text: btn_click(k))
        button.grid(row=1, column=column + 1)

del_button = tk.Button(
    keyboard_frames[1],
    text="DEL",
    bg="grey",
    fg="black",
    font=super_small_font,
    command=app.state.guess_rows[app.state.current_row].delete_char(),
)
del_button.grid(row=1, column=12)
window.bind("<BackSpace>", lambda event: app.state.guess_rows[app.state.current_row].delete_char())

enter_button = tk.Button(
    keyboard_frames[2],
    text="ENTR",
    bg="grey",
    fg="black",
    font=super_small_font,
    command=find_possible_words,
)
enter_button.grid(row=1, column=10)
window.bind("<Return>", lambda event: find_possible_words())

text_area = scrolledtext.ScrolledText(
    potential_words_frame, wrap=tk.WORD, width=50, height=30, state="disabled"
)
text_area.grid(row=0, column=0, sticky="nsew")

reset_button = tk.Button(
    potential_words_frame,
    text="Reset",
    bg="grey",
    fg="black",
    font=super_small_font,
    command=lambda: full_reset(),
)
reset_button.grid(row=1, column=0)

window.mainloop()
