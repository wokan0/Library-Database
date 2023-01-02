# Importing functions from other files
from menu import *
from database import *


# Creating database and books table with initial data
db = create_database()
cursor = db.cursor()

# Error handling in case table exists
try:
  create_table(db, cursor)
  # Creating list with inital data and adding to the table
  data = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
        (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
        (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
        (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

  add_entries(db, cursor, data)

except sqlite3.OperationalError: # Handling error that occurs if table exists
  pass

# Letting user input until they exit the loop
while True:
  print_menu()
  option = take_number()

  if option == 1:
    # Code to enter a new book
    id, title, author, qty = take_all_book_info()
    add_entries(db, cursor, [(id, title, author, qty)])
    
  elif option == 2:
    # Code to update book information
    # Code that asks for information about book to find it
    print("Enter information about book you want to update")
    old_data, columns = ask_for_book_info()
    # Code that asks for information that should be updated
    print("Enter data you want to update for the selected book")
    new_data, columns_to_update = ask_for_book_info()

    update_book(db, cursor, columns, old_data, columns_to_update, new_data) # Updating information

  elif option == 3:
    # Code to delete a book from the database
    # Code that asks for information about book to find it
    print("Enter information about book you want to delete")
    data, columns = ask_for_book_info()
    delete_book(db, cursor, columns, data)

  elif option == 4:
    # Code to search database for a book

    # Code that asks for information about book to find it
    print("Enter information about book you are looking for")
    data, columns = ask_for_book_info()
    books = search_book(cursor, columns, data)
    if len(books) == 0:
      print("No books are matching information given")
    else:
      print("{: >6} {: >70} {: >30} {: >8}".format("id", "Title", "Author", "Qty"))
      for book in books:
        print("{: >6} {: >70} {: >30} {: >8}".format(*book))

  elif option == 5:
    display_all(cursor)
  elif option == 0:
    break

  else:
    print("Wrong input, try again")
