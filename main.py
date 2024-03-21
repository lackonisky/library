import sqlite3
import hashlib
import pyfiglet
from simple_term_menu import TerminalMenu
import time
import os

def initialize():
	if os.path.exists("./library.db") == True:
		print(pyfiglet.figlet_format("Found"))
		database_connection()
	else:
		initialization = pyfiglet.figlet_format("System Initialization")
		print(initialization)
		create_database()

def create_database():
	# connects to the database and creates one if one is not already present
	connection = sqlite3.connect("library.db")
	# a database cursor is created so it can be used to execute SQL commands
	cursor = connection.cursor()
	# the cursor is used to execute the create table command within the database to create the books table
	cursor.execute("""CREATE TABLE "Books" (
		"BOOKNO"	INTEGER,
		"ISBN"	TEXT,
		"AUTHOR"	TEXT,
		"TITLE"	TEXT,
		"DATEPUBLISHED"	TEXT,
		"FORMAT"	TEXT,
		"STOCK"	INTEGER,
		"DESCRIPTION"	TEXT,
		PRIMARY KEY("BOOKNO" AUTOINCREMENT)
	);"""
	)
	# the cursor is used to execute the create table command within the database to create the users table
	cursor.execute("""CREATE TABLE "Users" (
		"IDNO"	INTEGER,
		"USERNAME"	TEXT,
		"PASS"	TEXT,
		"ACCESS"	INTEGER,
		PRIMARY KEY("IDNO" AUTOINCREMENT)
	);"""
	)
	connection.commit()
	username = input("""Enter the username you'd like to use for the base admin account""")
	password = input("""Enter the password you'd like to use for the base admin account""")
	password_hashing(password)
	cursor.execute("""INSERT INTO Users (USERNAME, PASS, ACCESS)
VALUES (?, ?, 1);""", (username, password,))
	connection.commit()
	initialize()

def database_connection():
    initializing = pyfiglet.figlet_format("Initialising")
    print(initializing)
    global connection
    connection = sqlite3.connect("library.db")
    global cursor
    cursor = connection.cursor()
    welcome = pyfiglet.figlet_format("Welcome to Benne's Library")
    # time.sleep(1.5)
    print(welcome)
    login()

def simple_menu():
    print("Main Menu")
    choices = ["Search Books", "View book list"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected ", choices[output])
    if output == 0:
        view_book()
    elif output == 1:
        item_list()
    else:
        menu_check()

def admin_menu():
    print("Admin Menu")
    choices = ["Search Books", "View Item list", "User Management", "Inventory Management"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        view_book()
    elif output == 1:
        item_list()
    elif output == 2:
        user_manager()
    elif output == 3:
        inventory()

def inventory():
    print("Inventory Management")
    choices = ["Add new item", "Update Inventory Stock", "Delete Item", "Edit Item", "Back"] 
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        new_item()
    elif output == 1:
        item_stock()
    elif output == 2:
        delete_item()
    elif output == 3:
        edit_item()
    elif output == 4:
        admin_menu()


def password_hashing(password): # function to hash the password and return the hash
    password = password.encode('utf-8')
    password = hashlib.sha3_256(password).hexdigest()
    return password

def login():
    time.sleep(0.5)
    print("""Login Portal
          """)
    username = input("Please input your username: ")
    password = input("Please enter your password: ")
    password = password_hashing(password)
    print(password)
    cursor.execute("SELECT PASS from Users WHERE USERNAME = ?", (username,))
    passw = cursor.fetchall()
    passw = str(passw[0][0])
    print(passw)
    if password == passw:
        cursor.execute("SELECT ACCESS from Users WHERE USERNAME = ?", (username,))
        global level
        level = cursor.fetchall()
        level = int(level[0][0])
        cursor.execute("SELECT IDNO from Users WHERE USERNAME = ? AND PASS = ?", (username, password,))
        global id
        id = cursor.fetchall()
        id = int(id[0][0])
        print(level)
        print(id)
        menu_check()

def menu_check():
    if level == 1:
        admin_menu()
    elif level == 0:
        simple_menu()
    else:
        login()

def book_search(): #################################################
    print("Book Search")
    choices = ["ISBN Search", "Name Search", "Author Search", "Book Number Search"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        bookinfo = ISBN_search()
    elif output == 1:
        bookinfo = Name_search()
    elif output == 2:
        bookinfo = Author_search()
    elif output == 3:
        bookinfo = book_number()
    return bookinfo

def view_book():
    bookinfo = book_search()
    print_item(bookinfo)

def book_number():
    try:
        num = input("input the book number ")
        cursor.execute("SELECT * from Books WHERE BOOKNO = ?",(num,))
        bookinfo = cursor.fetchall()
        bookinfo = bookinfo[0]
        return bookinfo
    except:
        print("Book not found or invalid input")
        menu_check()

def ISBN_search():###################
    try:
        isbn = input("input the book number ")
        cursor.execute("SELECT * from Books WHERE ISBN = ?",(isbn,))
        bookinfo = cursor.fetchall()
        bookinfo = bookinfo[0]
        return bookinfo
    except:
        print("Book not found or invalid input")
        menu_check()

def Name_search():#####################
    try:
        name = input("input the book number ")
        name = "%" + name + "%"
        cursor.execute("SELECT * from Books WHERE TITLE LIKE ?",(name,))
        bookinfo = cursor.fetchall()
        bookinfo = bookinfo[0]
        return bookinfo
    except:
        print("Book not found or invalid input")
        menu_check()
def Author_search(): ######################
    try:
        author = input("input the Authors name ")
        author = "%" + author + "%"
        cursor.execute("SELECT * from Books WHERE AUTHOR LIKE ?",(author,))
        bookinfo = cursor.fetchall()
        bookinfo = bookinfo[0]
        return bookinfo
    except:
        print("Book not found or invalid input")
        menu_check()

def user_manager():
    print("Account Manager")
    choices = ["Change Username", "Delete Account", "New Account"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        username_change()
    elif output == 1:
        if input("are you sure you want to delete your account y/n") == "y":
            delete_account()
        else:
            menu_check()
    elif output == 2:
        account_creation()

def new_item():
    itemName = input("Enter the Title of the item you'd like to add ")
    ISBN = input("Enter the ISBN of the item you'd like to add ")
    Author = input("Enter the Author of the item you'd like to add ")
    datePublished = input("Enter the Publishing date of the item you'd like to add in the format DD/MM/YYYY ")
    itemFormat = input("Enter the Format of the item you'd like to add ")
    while True:
        stockLevel = input("Enter the stock level of the item you'd like to add ")
        if stockLevel.isnumeric():
            break
    itemDescription = input("Enter a description of the item you'd like to add")
    adding = """Title: {}
ISBN: {}
Author: {}
Date Published: {}
Item Format: {}
Stock Level: {}
Item Description: {}
    """.format(itemName, ISBN, Author, datePublished, itemFormat, stockLevel, itemDescription)
    print(adding)
    check = ["Yes", "No"]
    menu = TerminalMenu(check)
    output = menu.show()
    if output == 0:
        cursor.execute("""INSERT INTO Books (ISBN, AUTHOR, TITLE, DATEPUBLISHED, FORMAT, STOCK, DESCRIPTION)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", (ISBN, Author, itemName, datePublished, itemFormat, stockLevel, itemDescription,))
        connection.commit()
        print("succesful")
        inventory()

def item_stock():
    book = book_search()
    print(book[3], ",", book[2])
    print("Stock: ", book[6])
    menu_check()

def delete_item():##################
    menu_check()

def item_list():
    cursor.execute("SELECT * FROM Books")
    items = cursor.fetchall()
    print(len(items))
    for n in range(0, len(items)):
        item = """Book Number: {}
Title: {}
ISBN: {}
Author: {}
Date Published: {}
Item Format: {}
Stock Level: {}
Item Description: {}
    """.format(items[n][0], items[n][1], items[n][2], items[n][3], items[n][4], items[n][5], items[n][6], items[n][7])
        print(item, """
          """)
    menu_check()



def edit_item():
    while True:
        bookNum = input("Enter the stock level of the item you'd like to add ")
        if bookNum.isnumeric():
            break
    itemName = input("Enter the new Title of the item you'd like to change ")
    ISBN = input("Enter the new ISBN of the item you'd like to change ")
    Author = input("Enter the new Author of the item you'd like to change ")
    datePublished = input("Enter the new Publishing date of the item you'd like to change in the format DD/MM/YYYY ")
    itemFormat = input("Enter the new Format of the item you'd like to change ")
    while True:
        stockLevel = input("Enter the stock level of the item you'd like to add ")
        if stockLevel.isnumeric():
            break
    itemDescription = input("Enter a new description for the item you'd like to change")
    changing = """Title: {}
ISBN: {}
Author: {}
Date Published: {}
Item Format: {}
Stock Level: {}
Item Description: {}
    """.format(itemName, ISBN, Author, datePublished, itemFormat, stockLevel, itemDescription)
    print(changing)
    check = ["Yes", "No"]
    menu = TerminalMenu(check)
    output = menu.show()
    if output == 0:
        cursor.execute("""UPDATE Books
SET ISBN = ? ,
    AUTHOR = ? ,
    TITLE = ? ,
    DATEPUBLISHED = ? ,
    FORMAT = ? ,
    STOCK = ? ,
    DESCRIPTION = ?
WHERE BOOKNO = ?;
""", (ISBN, Author, itemName, datePublished, itemFormat, stockLevel, itemDescription, bookNum))
        connection.commit()
        print("succesful")
        inventory()
    else:
        menu_check()

def delete_account():
    cursor.execute("""DELETE FROM BOOKS
WHERE IDNO = ?""", (id,))
    connection.commit()
    menu_check()

def username_change():
    if level == 1:
        changed_user = input("Enter the username of the account you'd like to change")
        change_to = input("Enter the username you'd like to change it to")
        cursor.execute("SELECT USERNAME from Users WHERE USERNAME = ?", (change_to,))
        available = cursor.fetchall()
        print(available)
        cursor.execute("UPDATE Users SET USERNAME = ? WHERE USERNAME = ?")
#    elif level == 2:


def print_item(bookinfo):
    item = """Book Number: {}
Title: {}
ISBN: {}
Author: {}
Date Published: {}
Item Format: {}
Stock Level: {}
Item Description: {}
    """.format(bookinfo[0], bookinfo[3], bookinfo[1], bookinfo[2], bookinfo[4], bookinfo[5], bookinfo[6], bookinfo[7])
    print(item, """
          """)
    menu_check()

def account_creation():
    
    while True:
        uName = input("Enter the username of the account youd like to create ")
        cursor.execute("SELECT * from Users WHERE Username = ?", (uName,))
        taken = cursor.fetchall()
        if not taken:
            break
    while True:
        passw = input("Please input your password")
        passcheck = input("Please repeat your password")
        if passw == passcheck:
            break
    passw = password_hashing(passw)
    cursor.execute("""INSERT INTO Users (USERNAME, PASS, ACCESS)
                   
VALUES(?, ?, ?);""", (uName, passw, 0,))
    connection.commit()
    print("Account Created")
    menu_check()


initialize()