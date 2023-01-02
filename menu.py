def check_number(number):  # Checks if input is a number
    try:
        float(number)
        return True
    except ValueError:
        print("Input isn't a valid number, try again.")
        return False

# Function to take input from user and check if it matches a value in args
def take_letter(*args):
    while True:
        letter = input("Enter [{}]: ".format("/".join(args)))
        if letter in args:
            return letter
        else:
            print("Try again.")

# Takes input and checks if it is a number
def take_number():
    while True:
        number = input("Enter a number: ")
        if check_number(number):
            break
        else:
            print("Try again.")
    return int(float(number))

# Takes y/n input and converts to bool
def letter_to_bool(letter):
    if letter == 'y':
        return True
    else:
        return False


# Prints menu options
def print_menu():
    print("\n\nEnter number to select an option")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book") 
    print("4. Search book")
    print("5. Show all books")
    print("0. Exit\n\n")

# Function to ask user for desired book information
def take_all_book_info(id=True, title=True, author=True, qty=True):
    if id:
        print("Enter id of the book ")
        yield take_number()
    if title:
        yield input("Enter title of the book ")
    if author:
        yield input("Enter author of the book ")
    if qty:
        print("Enter quantity of the book ")
        yield take_number()

# Function that asks which information user wants to enter and returns it
# together with names of columns for that data
def ask_for_book_info():
    columns = ['id', 'Title', 'Author', 'Qty'] # List with all column names
    columns_entered = []
    checks = {}
    book_info = []
    for col in columns:
      # Ask user if they want to update each column
      print("Do you want to enter {}? [y/n]".format(col))
      checks[col] = letter_to_bool(take_letter('y', 'n'))
      # Add those to the list that will be passed to the database function
      if checks[col] == True:
        columns_entered.append(col)

    for info in take_all_book_info(*list(checks.values())):
        book_info.append(info)
    
    return book_info, columns_entered