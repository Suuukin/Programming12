import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as font
import wordlist

# This is a modified version of the original template Mr. Poy
# created. This version is for displaying a list of words
# that meets the criteria of the wordle you are playing

window = tk.Tk()
window.title("Wordle Cheater")
window.resizable(False, False)

large_font = font.Font(family="Courier", size=40, weight="bold")
small_font = font.Font(family="Courier", size=20, weight="bold")
super_small_font = font.Font(family="Courier", size=20, weight="bold")


class Wordle:
    def __init__(self):
        self.letter_count = 0
        self.game_over = False
        self.word = ""
        self.guess = ""


wordle = Wordle()


def create_label(frame=window):
    # Create a Tkinter Label
    new_label = tk.Label(
        frame,
        text=" ",
        bg="white",
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
        bg="white",
        fg="black",
        font=small_font,
        command=lambda: btn_click(letter),
    )
    return new_button


def btn_click(letter):
    guess_labels[wordle.letter_count]["text"] = letter
    wordle.guess += letter
    print(wordle.guess)

    if wordle.letter_count < 5:
        wordle.letter_count += 1


def delete_char():
    # This function will delete the current letter
    # Use a class variable (wordle.letter_count) to keep track of which label to erase
    # go back a spot as long as you are not in the first spot
    print("delete")
    if wordle.letter_count != 0:
        wordle.letter_count -= 1
        wordle.guess = wordle.guess[:-1]
        guess_labels[wordle.letter_count]["text"] = " "
        guess_labels[wordle.letter_count]["bg"] = "white"


def color_label(color):
    if wordle.letter_count == 0:
        label_position = wordle.letter_count
    else:
        label_position = wordle.letter_count - 1

    guess_labels[label_position]["bg"] = color


def letter_check(letter_color, letter, word, letter_position):
    if letter_color == "white":
        if letter not in word:
            return False
    elif letter_color == "yellow":
        if letter in word and word[letter_position] != letter:
            return False
    elif letter_color == "green":
        if word == "basic":
            print(
                f"word = {word}, letter_word = {word[letter_position]} letter = {letter}"
            )
        if letter in word and word[letter_position] == letter:
            return False
    return True


def find_possible_words():
    text_area.configure(state="normal")
    possible_words = wordlist.wordle_list
    for i, letter in enumerate(wordle.guess):
        letter_color = guess_labels[i]["bg"]
        for word in possible_words:
            remove_word = letter_check(letter_color, letter, word, i)
            if remove_word:
                possible_words.remove(word)
                print(f"removing {word}, because {letter_color, letter, i, word[i]}")
            else:
                print(f"keeping {word}, because {letter_color, letter, i, word[i]}")
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, possible_words)
    text_area.configure(state="disabled")


# Create 30 labels in a 5 x 6 grid starting at label[0]..label[29]
# start with an empty dictionary --> label={}  then loop through 30 of them

guess_frame = tk.Frame(window)
guess_frame.pack(side=tk.TOP)

keyboard_frame = tk.Frame(window)
keyboard_frame.pack(side=tk.TOP)

potential_words_frame = tk.Frame(window)
potential_words_frame.pack(side=tk.TOP)

guess_labels = {}
for i in range(0, 5):
    guess_labels[i] = create_label(guess_frame)
    # place the label at an x,y position
    guess_labels[i].grid(row=0, column=i)

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
        button.bind(str(key_text), lambda: btn_click(key_text))
        button.grid(row=1, column=column + 1)

del_button = tk.Button(
    keyboard_frames[1],
    text="DEL",
    bg="white",
    fg="black",
    font=super_small_font,
    command=delete_char,
)
del_button.grid(row=1, column=12)

enter_button = tk.Button(
    keyboard_frames[2],
    text="ENTR",
    bg="white",
    fg="black",
    font=super_small_font,
    command=find_possible_words,
)
enter_button.grid(row=1, column=10)

yellow_button = tk.Button(
    guess_frame,
    text=" ",
    bg="yellow",
    fg="black",
    font=super_small_font,
    command=lambda: color_label("yellow"),
)
yellow_button.grid(row=0, column=6)

green_button = tk.Button(
    guess_frame,
    text=" ",
    bg="green",
    fg="black",
    font=super_small_font,
    command=lambda: color_label("green"),
)
green_button.grid(row=0, column=7)

text_area = scrolledtext.ScrolledText(
    potential_words_frame, wrap=tk.WORD, width=50, height=30
)
text_area.grid(row=0, column=0, sticky="nsew")

window.mainloop()
