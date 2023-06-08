# TODO
def main():
    change = get_change()
    cents = round(change * 100)
    quarters = 0
    dimes = 0
    nickels = 0
    pennies = 0

    # calculate quarters
    while cents >= 25:
        cents = cents - 25
        quarters += 1

    # calculate dimes
    while cents >= 10:
        cents = cents - 10
        dimes += 1

    # calculate nickels
    while cents >= 5:
        cents = cents - 5
        nickels += 1

    # calculate pennies
    while cents >= 1:
        cents = cents - 1
        pennies += 1

    # add and print total of all coins
    coins = quarters + dimes + nickels + pennies
    print(coins)


def get_change():
    change = 0
    while change <= 0:
        try:
            # get valid input from user
            change = float(input("Change owed:"))
            if change > 0:
                return change
        except ValueError:
            print("Input change owed")


main()
