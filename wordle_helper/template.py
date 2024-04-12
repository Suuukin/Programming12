import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as font
import wordlist
import random

# This is a modified version of the original template Mr. Poy
# created. This version is for displaying a list of words
# that meets the criteria of the wordle you are playing

window = tk.Tk()
window.title("Wordle Cheater")
window.geometry("570x720")
large_font = font.Font(family="Courier", size=40, weight="bold")
small_font = font.Font(family="Courier", size=20, weight="bold")
super_small_font = font.Font(family="Courier", size=20, weight="bold")


class Wordle:
    def __init__(self):
        self.position = 0
        self.game_over = False
        self.word = ""
        self.guess = ""


wordle = Wordle()
wordle.word = random.choice(wordlist.wordle_list).upper()
print(wordle.word)


def create_label():
    # Create a Tkinter Label
    new_label = tk.Label(
        window,
        text=" ",
        bg="white",
        fg="black",
        font=large_font,
        borderwidth=2,
        relief="solid",
    )
    return new_label


def create_button(letter):
    # Create a Tkinter Label
    new_button = tk.Button(
        window,
        text=letter,
        bg="white",
        fg="black",
        font=small_font,
        command=lambda: btn_click(letter),
    )
    return new_button


def btn_click(letter):
    # place the letter in the appropriate label
    # you figure out the code
    # below is an example of what you could do

    label[wordle.position]["text"] = letter

    if wordle.position < 5:
        wordle.position += 1


def delete_char():
    # This function will delete the current letter
    # Use a class variable (wordle.position) to keep track of which label to erase
    # go back a spot as long as you are not in the first spot
    beginning_of_line = [0]
    if (
        label[wordle.position]["text"] == " "
        and wordle.position not in beginning_of_line
    ):
        wordle.position -= 1
    label[wordle.position]["text"] = " "
    label[wordle.position]["bg"] = "white"


def make_green():
    if wordle.position > 0:
        wordle.position -= 1
    label[wordle.position]["bg"] = "green"
    if wordle.position < 4:
        wordle.position += 1


def make_yellow():
    if wordle.position > 0:
        wordle.position -= 1
    label[wordle.position]["bg"] = "yellow"
    if wordle.position < 4:
        wordle.position += 1


def guess():
    # use this function to update the display list of words
    print("Checking the wordle to see if the row of labels = wordle")
    print(wordle.guess)
    # you will use code using the wordle.guess to find the possible word list
    # then display the possible word list into the text area
    # the sample code below searches just the first 1000 words from the wordlist
    # and adds it to the temporary list if there is a "e" somewhere
    possible_words = []
    for index in range(0, 1000):
        if "e" in wordlist.wordle_list[index]:
            possible_words.append(wordlist.wordle_list[index])
    text_area.insert(tk.END, possible_words)

    # Disable editing of the text box
    text_area.configure(state="disabled")


# Create 30 labels in a 5 x 6 grid starting at label[0]..label[29]
# start with an empty dictionary --> label={}  then loop through 30 of them
label = {}
pos_x = 0
pos_y = 0
for i in range(0, 5):
    label[i] = create_label()
    pos_x += 45
    # place the label at an x,y position
    label[i].place(x=165 + pos_x, y=10 + pos_y)

# Create a keyboard
# start with an empty dictionary called button = {}, then add elements button[1] etc
button = {}
pos_x = 0
pos_y = 0
row_chars = "QWERTYUIOP "
for i, c in enumerate(row_chars):
    button[i] = create_button(c)
    pos_x += 45
    button[i].place(x=10 + pos_x, y=500)
row_chars = "ASDFGHJKL"
pos_x = 0
pos_y = 0
for i, c in enumerate(row_chars):
    button[i] = create_button(c)
    pos_x += 45
    button[i].place(x=0 + pos_x, y=570)
row_chars = "ZXCVBNM"
pos_x = 0
pos_y = 0
for i, c in enumerate(row_chars):
    button[i] = create_button(c)
    pos_x += 45
    button[i].place(x=10 + pos_x, y=640)

del_button = tk.Button(
    window,
    text="DEL",
    bg="white",
    fg="black",
    font=super_small_font,
    command=delete_char,
)
del_button.place(x=450, y=570)

enter_button = tk.Button(
    window,
    text="ENTR",
    bg="white",
    fg="black",
    font=super_small_font,
    command=guess,
)
enter_button.place(x=370, y=640)

green_button = tk.Button(
    window,
    text=" ",
    bg="green",
    fg="black",
    font=super_small_font,
    command=make_green,
)
green_button.place(x=464, y=640)

yellow_button = tk.Button(
    window,
    text=" ",
    bg="yellow",
    fg="black",
    font=super_small_font,
    command=make_yellow,
)
yellow_button.place(x=510, y=640)

text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
text_area.place(x=10, y=90, width=540, height=400)

window.mainloop()
