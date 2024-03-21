#import the sqlite3 library so it can be used to interact with the database
import sqlite3
import os
import hashlib 
import pyfiglet

def initialize():
	if os.path.exists("./library2.db") == True:
		print("Database Found")
		login()
	else:
		initialization = pyfiglet.figlet_format("System Initialization")
		print(initialization)
		create_database()

def password_hashing(password): # function to hash the password and return the hash
    password = password.encode('utf-8')
    password = hashlib.sha3_256(password).hexdigest()
    return password

def create_database():
	# connects to the database and creates one if one is not already present
	connection = sqlite3.connect("library2.db")
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

initialize()