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


def main():
    print(
        'You can convert from any 2 of these 4 temperature scales "Celsius, Fahrenheit, Kelvin, Rankine." '
    )

    input_line = input(
        'What would you like to convert? Enter in the format "14 C in K". '
    )
    number, unit_1, placeholder, unit_2 = input_line.split(" ") # split on space
    result = temp_calc(float(number), unit_1, unit_2)
    print(f"{float(number)} {unit_1} is equal to {result:.2f} {unit_2}.")


if __name__ == "__main__":
    main()
