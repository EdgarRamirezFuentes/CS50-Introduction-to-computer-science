from cs50 import get_int
if __name__ == "__main__":
    while True:
        # Gets the height of the pyramid from user
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break
    # Loops row by row of the pyramid
    for i in range(1, height + 1):
        # Prints the empty spaces of current row
        print(" " * (height - i), end="")
        # Prints the hash tags of the current row
        print("#" * i, end="")
        # Prints the second pyramid
        print("  " + "#" * i)
