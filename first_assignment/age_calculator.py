from datetime import date


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


def main():
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


if __name__ == "__main__":
    main()
