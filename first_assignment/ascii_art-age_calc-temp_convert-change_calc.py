from datetime import date

KELVIN = None


def temp_calc(input_number, starting_unit, return_unit):
    if starting_unit == "C":
        print(input_number)
        KELVIN = input_number + 273.15
        print(KELVIN)
    elif starting_unit == "F":
        KELVIN = input_number * (5 / 9) - 459.67
    elif starting_unit == "R":
        KELVIN = input_number * (5 / 9)
    else:
        KELVIN = input_number

    if return_unit == "C":
        output = KELVIN - 273.15
    elif return_unit == "F":
        output = KELVIN / (5 / 9) - 459.67
    elif return_unit == "R":
        output = KELVIN / (5 / 9)
    else:
        print(f"output = {KELVIN}")
        output = KELVIN

    return output


def main():
    # user selects which section they want to use
    section = input("What do you want to do (art, age, temp, coin)? ")

    if section == "art":
        return

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
                "Please enter the future date you would like to check in the format year/month/day ie. 2034/7/25. "
            )
        # split the date
        future_year, future_month, future_day = future_date.split("/")

        birth_date = input(
            "Please enter your birthdate in the format year/month/day ie. 2000/3/15. "
        )
        # split the date
        birth_year, birth_month, birth_day = birth_date.split("/")

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
            if int(birth_day) < int(future_day):
                age_year -= 1

        print(f"You are {age_year} years and {age_month} months old.")

    if section == "temp":

        print(
            'You can convert from any 2 of these 4 temperature scales "Celsius, Fahrenheit, Kelvin, Rankine." '
        )

        input_line = input(
            'What would you like to convert? Enter in the format "14 C in K". '
        )
        number, unit_1, foo, unit_2 = input_line.split(" ")
        result = temp_calc(float(number), unit_1, unit_2)
        print(f"{float(number)} {unit_1} is equal to {result} {unit_2}.")
        return

    if section == "coin":
        return


if __name__ == "__main__":
    main()
