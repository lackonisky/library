mport sqlite3
import hashlib
import pyfiglet
from simple_term_menu import TerminalMenu
import time
initialising = pyfiglet.figlet_format("Initialising")
print(initialising)
connection = sqlite3.connect("library3.db")
cursor = connection.cursor()
welcome = pyfiglet.figlet_format("Welcome to Benne's Library")
# time.sleep(1.5)
print(welcome)

def simple_menu():
    print("Main Menu")
    choices = ["Search Books", "View book list", "Account Management"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected ", choices[output])

def admin_menu():
    print("Admin Menu")
    choices = ["Search Books", "View Item list", "Account Management", "User Management", "Inventory Management"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        book_search()
    elif output == 1:
        item_list()
    elif output == 2:
        account_manager()
    elif output == 3:
        user_manager()
    elif output == 4:
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
    # time.sleep(2)
    print("""Login Portal
          """)
    username = input("Please input your username")
    password = input("Please enter your password")
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
    if id == 1:
        admin_menu()
    elif id == 0:
        simple_menu()
    else:
        login()

def book_search(): #################################################
    print("Book Search")
    choices = ["ISBN Search", "Name Search", "Author Search"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        ISBN_search()
    elif output == 1:
        Name_search()
    elif output == 2:
        Author_search()

def ISBN_search():###################
    exit

def Name_search():#####################
    exit

def Author_search(): ######################
    exit

def account_manager():
    print("Account Manager")
    choices = ["Change Username", "Delete Account"]
    menu = TerminalMenu(choices)
    output = menu.show()
    print("You selected", choices[output], """ 
          """)
    if output == 0:
        username_change()
    elif output == 1:
        if input("are you sure you want to delete your account y/n") == y:
            delete_account()
        else:
            menu_check()



def new_item():
    itemName = input("Enter the Title of the item you'd like to add ")
    ISBN = input("Enter the ISBN of the item you'd like to add ")
    Author = input("Enter the Author of the item you'd like to add ")
    datePublished = input("Enter the Publishing date of the item you'd like to add in the format DD/MM/YYYY ")
    itemFormat = input("Enter the Format of the item you'd like to add ")
    stockLevel = int(input("Enter the stock level of the item you'd like to add "))
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


def item_stock():#####################
    exit

def delete_item():##################
    exit

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

def user_manager():
    exit

def edit_item():
    exit



def loaned_books():
    exit

def loan_history():
    exit

def username_change():
    if level == 1:
        changed_user = input("Enter the username of the account you'd like to change")
        change_to = input("Enter the username you'd like to change it to")
        cursor.execute("SELECT USERNAME from Users WHERE USERNAME = ?", (change_to,))
        available = cursor.fetchall()
        print(available)
        cursor.execute("UPDATE Users SET USERNAME = ? WHERE USERNAME = ?")
    #######################################################
    #######################################################
  
login()
