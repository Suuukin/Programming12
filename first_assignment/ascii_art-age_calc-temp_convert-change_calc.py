from datetime import date

MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

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
            # change date format from yyyy-mm-dd to yyyy/mm/dd
            future_date = future_date.replace("-", "/")
        else:
            future_date = input(
                "Please enter the future date you would like to check in the format year/month/day ie. 2034/7/25. "
            )

        future_year, future_month, future_day = future_date.split("/")
        birth_date = input(
            "Please enter your birthdate in the format year/month/day ie. 2000/3/15. "
        )
        birth_year, birth_month, birth_day = birth_date.split("/")

        age_year = int(future_year) - int(birth_year)
        age_month = int(future_month) - int(birth_month)
        # age_day = int(future_day) - int(birth_day)

        if int(future_month) < int(birth_month):
            age_year -= 1
            age_month += 12
        if int(future_month) == int(birth_month):
            if int(birth_day) < int(future_day):
                age_year -= 1
        print(f"You are {age_year} years and {age_month} months old.")

    if section == "temp":
        return

    if section == "coin":
        change = input("How much change total are you expecting? ")
        return


if __name__ == "__main__":
    main()
