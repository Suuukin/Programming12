import decimal as dec
import math

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
    money = dec.Decimal(input("How much money do you need in change (243.12)? "))
    change = change_calc(money) # returns dict
    change_string = f"You have ${money}"
    for denomination in change:
        change_string += f" {change[denomination]} {denomination}"
    print(change_string)

if __name__ == "__main__":
    main()
