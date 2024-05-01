key = "GI"

# The word CAT ===> A ---> G  code up A-(1)B-(2)C-(3)D-(4)E-(5)F-(6)G
word = input("What word would you like to encrypt or decrypt? ")
shift = int(
    input("How many characters do you wish to shift? For right use negative (-7). ")
)

letter_list = ["abcdefghijklmnopqrstuvwxyz"]

alphabet_dict = {}
for alphabet in letter_list:
    for i, letter in enumerate(alphabet):
        alphabet_dict[i + 1] = letter

new_word = ""
for char in word.lower():
    for value, letter in alphabet_dict.items():
        if letter == char:
            final_value = value + shift
            if final_value <= 0:
                final_value += 26
            elif final_value > 26:
                final_value -= 26
            final_char = alphabet_dict[final_value]
    new_word = new_word + final_char
    print(f"The code value of '{char}' is", ord(char))
    print(
        f"'{char}' coded by {shift} more is {final_value} or letter '{final_char}'  "
    )

# loop is done
print(f"The encoded {word} is now {new_word.upper()}")
