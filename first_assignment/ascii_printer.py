FONT = { 
    "A": " ###  " 
         "#   # "
         "##### "
         "#   # "
         "#   # ",
 
    "B": "####  "
         "#   # "
         "####  "
         "#   # "
         "####  ",
 
    "C": " #### "
         "#     "
         "#     "
         "#     "
         " #### ",
 
    "D": "###   "
         "#  #  "
         "#   # "
         "#  #  "
         "###   ",
 
    "E": "##### "
         "#     "
         "##### "
         "#     "
         "##### "
}

def word_buffer(input_word):
    letter_rows = 5  # number of rows per letter in FONT
    letter_columns = 6  # number of columns per letter in FONT
    total_columns = letter_columns * len(input_word)

    buffer = []  # buffer to create rows before printing
    for i in range(letter_rows):
        # creating nested lists inside of the buffer list
        # filled with empty strings
        buffer.append([""] * total_columns)

    for char_number, char in enumerate(input_word):
        # for each letter need to move to not overwrite
        column = (
            char_number * letter_columns
        )  
        character = FONT[char]
        for x in range(letter_rows):
            for y in range(letter_columns):
                """
                imagine buffer as x,y grid, it is a nested list
                first you take the row list, then fill the required column
                with either the inputted character or a space
                """
                char_or_space = character[x * letter_columns + y] 
                if char_or_space == "#":
                    char_or_space = char
                buffer[x][column + y] = char_or_space
    return buffer


def main():
    word = input("What would you like to print using only the letters abcde e.g. bed? ")
    word = word.upper()  # uppercase word to act as key in dict
    buffer = word_buffer(word)
    for row in buffer:
        # start with empty string then add each row list from the buffer
        print("".join(row))


if __name__ == "__main__":
    main()
