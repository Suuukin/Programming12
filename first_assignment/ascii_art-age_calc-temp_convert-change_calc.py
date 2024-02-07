from datetime import date
import math
import decimal as dec

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
                # imagine buffer as x,y grid it is a nested list
                # first you take the row list, then fill the required column
                # with the symbol for the character at that location
                buffer[x][column + y] = character[x * letter_columns + y]
    return buffer

def age_calc(future_date, birth_date):
    # split the date
    birth_year, birth_month, birth_day = birth_date.split("/")

    # split the date
    future_year, future_month, future_day = future_date.split("/")

    # calculate the age in years
    age_year = int(future_year) - int(birth_year)
    age_month = int(future_month) - int(birth_month)

    # if before their birthday this year
    if int(future_month) < int(birth_month):
        age_year -= 1
        age_month += 12

    # if their birthday is in the same month
    if int(future_month) == int(birth_month):
        # if it's before their birthday in that month
        if int(birth_day) > int(future_day):
            age_year -= 1
            
    return age_year, age_month

def temp_calc(input_number, starting_unit, return_unit):
    """
    Converts any input temperature unit to Kelvin then
    converts to the required output unit. 
    """
    kelvin = None
    if starting_unit == "C":
        print(input_number)
        kelvin = input_number + 273.15
        print(kelvin)
    elif starting_unit == "F":
        kelvin = input_number * (5 / 9) + 459.67
    elif starting_unit == "R":
        kelvin = input_number * (5 / 9)
    else:
        kelvin = input_number

    if return_unit == "C":
        output = kelvin - 273.15
    elif return_unit == "F":
        output = (kelvin / (5 / 9)) - 459.67
    elif return_unit == "R":
        output = kelvin / (5 / 9)
    else:
        print(f"output = {kelvin}")
        output = kelvin
    return output


def change_calc(money):    
    """
    Takes input money and returns the required
    change coins, preferring biggest denominations first.
    """
    change = {} # dict to hold the type and number of change
    currency_denominations = { # dict of name and coin value
        "hundreds": "100",
        "fifties": "50",
        "twenties": "20",
        "tens": "10",
        "fives": "5",
        "toonies": "2",
        "loonies": "1",
        "quarters": "0.25",
        "dimes": "0.1",
        "nickels": "0.05",
        "pennies": "0.01",
    }

    for denomination in currency_denominations:
        """
        Go from biggest to smallest denomination and divide
        to see how many can fit. Round down to whole number
        then subtract the total value of change from money and
        add to change dictionary. 
        """
        currency_value = dec.Decimal(currency_denominations[denomination])
        if money >= currency_value: 
            change_number = dec.Decimal(money) / currency_value 
            change_number = math.floor(change_number) 
            money -= change_number * currency_value 
            change[denomination] = change_number 
    return change

def main():
    # user selects which section they want to use
    section = input("What do you want to do (art, age, temp, coin)? ")

    if section == "art":
        word = input("What would you like to print using only the letters abcde e.g. bed? ")
        word = word.upper()  # uppercase word to act as key in dict
        buffer = word_buffer(word)
        for row in buffer:
            # start with empty string then add each row list from the buffer
            print("".join(row))


    if section == "age":
        use_current_date = input(
            "Do you want to find your age today or your age in the future (today, future)? "
        )

        # use the datetime module to get the current date yyyy-mm-dd
        if use_current_date == "today":
            future_date = str(date.today())
            # change date format to be seperated by slashes rather than hyphens
            future_date = future_date.replace("-", "/")
        else:
            future_date = input(
                "Please enter the future date you would like to check in the format year/month/day e.g. 2034/7/25. "
            )

        birth_date = input(
            "Please enter your birthdate in the format year/month/day e.g. 2000/3/15. "
        )

        age_year, age_month = age_calc(future_date, birth_date)

        print(f"You are {age_year} years and {age_month} months old.")

    if section == "temp":
        print(
            'You can convert from any 2 of these 4 temperature scales "Celsius, Fahrenheit, Kelvin, Rankine." '
        )

        input_line = input(
            'What would you like to convert? Enter in the format "14 C in K". '
        )
        number, unit_1, placeholder, unit_2 = input_line.split(" ") # split on space
        result = temp_calc(float(number), unit_1, unit_2)
        print(f"{float(number)} {unit_1} is equal to {result:.2f} {unit_2}.")

    if section == "coin":
        money = dec.Decimal(input("How much money do you need in change (243.12)? "))
        change = change_calc(money) # returns dict
        change_string = f"You have ${money}"
        for denomination in change:
            change_string += f" {change[denomination]} {denomination}"
        print(change_string)


if __name__ == "__main__":
    main()
