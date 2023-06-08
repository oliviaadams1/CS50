def main():
    height = get_height()
    for i in range(height):
        i += 1
        k = height - i
        print(" " * k, end="") #spacing on left side the pyramid
        print("#" * i) #print hashes for pyramid based on user input 


def get_height():
    n = 0
    while n <= 0 or n > 8:
        try:
            n = int(input("Height: "))  # get height from user
            if n > 0 and n <= 8:  # height between 1 and 8
                return n
        except ValueError:  # reprompt for numerical height if user inputs a letter
            print("Input an integer")


main()
