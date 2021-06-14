from cs50 import get_float
import math

if __name__ == "__main__":
    # The amount of money of each coin
    coins = [25, 10, 5, 1]
    # The number of coins returned to pay the owed money
    change_coins = 0
    while True:
        change = get_float("Change owed: ")
        # Only accepts positive change
        if change > 0:
            break
    change = round(change * 100)
    for coin in coins:
        # Get the max number of coins that fit into the remaining change
        change_coins += int(change / coin)
        # Update the remaipytning change owed
        change -= int(change / coin) * coin

    print(change_coins)
