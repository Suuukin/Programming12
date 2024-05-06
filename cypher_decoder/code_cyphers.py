# The word CAT ===> A ---> G  code up A-(1)B-(2)C-(3)D-(4)E-(5)F-(6)G
word = input("What word would you like to encrypt or decrypt? ")
key = input("Enter a key or number for how much you want to shift (ag), (4), (-7). ")


letter_list = ["abcdefghijklmnopqrstuvwxyz"]

alphabet_dict = {}
for alphabet in letter_list:
    for i, letter in enumerate(alphabet):
        alphabet_dict[i + 1] = letter

if key.isnumeric():
    shift = int(key)
else:
    key_values = []
    for letter in list(key.lower()):
        for value, char in alphabet_dict.items():
            if letter == char:
                key_values.append(value)
    shift = key_values[1] - key_values[0]


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
    # print(f"The code value of '{char}' is", ord(char))
    # print(f"'{char}' coded by {shift} more is {final_value} or letter '{final_char}'  ")

# loop is done
print(f"The encoded {word} is now {new_word.upper()}")
