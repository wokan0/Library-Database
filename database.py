# Importing libraries
import sqlite3

# Function to create database
def create_database():
    return sqlite3.connect("ebookstore")

# Function to create empty table (id, Title, Author, Qty) and commiting the changes
def create_table(db, cursor):
    cursor.execute('''CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')
    db.commit()

# Function that takes database, cursor and list of tuples with (id, Title, Author, Qty) and adds all to the database
def add_entries(db, cursor, *args):
    try:
        cursor.executemany('''INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)''', args[0])
        db.commit()
        print("New book added")
    except sqlite3.IntegrityError: # Handling error in case id is already taken
        print("the id is already taken by another book, can't create new record")


# Function to create a select all query, given column names used in the query
# args format: [col1_name, col2_name, ...]
# Example: ['id', 'Title']
def select_query(*args):
    query = "SELECT * FROM books WHERE "
    for col in args[0]:
        query += (col + " = ? AND ")
    query = query[:-5] # Removing ' AND ' from the end of the query
    return query

# Function to create an uodate query, given column names used in the query
# args format: [col1_name, col2_name, ...]
# Example: ['Title', 'Author']
def update_query(*args):
    query = "UPDATE books SET "
    for col in args[0]:
        query += (col + " = ?, ")
    query = query[:-2] # Removing ', ' from the end of the query
    query += " WHERE id = ?"
    return query

# Function to search for a book, given information about it
# args format: [[col1_name, col2_name, ...], [col1_val, col2_val, ...]]
# Example: [['id', 'Title'], [3001, 'A Tale of Two Cities']]
def search_book(cursor, *args):
    books = []
    query = select_query(args[0])
    cursor.execute(query, args[1])
    for book in cursor:
        books.append(book)
    return books

# Function to update book information
# args format: [[col1_search, col2_search...], [val1_old, val2_old...], [col1_update, col2_update...], [val1_new, val2_new...]]
# Example: [['id'], [3001], ['Title', 'Author'], ['new title', 'new Author']]
def update_book(db, cursor, *args):
    book = search_book(cursor, args[0], args[1])
    # Checking if only one book matches information given
    if len(book) > 1:
        print("More than one book matching information, try again")
        return
    elif len(book) == 0:
        print("No books matching information, try again")
        return
    
    query = update_query(args[2])
    args[3].append(book[0][0]) # Creating a list with values to update and id (book[0]) for the query
    # Handling error in case updated id is not unique
    try:
        cursor.execute(query, args[3])
        db.commit()
        print("Book information updated")
    except sqlite3.IntegrityError:
        print("New id is already taken by another book, can't update the information")

# Function to delete a book, given information about it
# args format: [[col1_name, col2_name, ...], [col1_val, col2_val, ...]]
# Example: [['id', 'Title'], [3001, 'A Tale of Two Cities']]
def delete_book(db, cursor, *args):
    book = search_book(cursor, args[0], args[1])
    # Checking if only one book matches information given
    if len(book) > 1:
        print("More than one book matching information, try again")
        return
    elif len(book) == 0:
        print("No books matching information, try again")
        return
    id = book[0][0]

    cursor.execute('''DELETE FROM books WHERE id=?''', (id, ))
    db.commit()
    print("Book deleted")

# Function to display all records
def display_all(cursor):
    cursor.execute('''SELECT * FROM books''')
    print("{: >6} {: >70} {: >30} {: >8}".format("id", "Title", "Author", "Qty"))
    for book in cursor:
        print("{: >6} {: >70} {: >30} {: >8}".format(*book))

