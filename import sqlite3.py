#import the sqlite3 library so it can be used to interact with the database
import sqlite3
# connects to the database and creates one if one is not already present
connection = sqlite3.connect("library5.db")
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
cursor.execute("""INSERT INTO Users (USERNAME, PASS, ACCESS)
VALUES ('admin', 'fb001dfcffd1c899f3297871406242f097aecf1a5342ccf3ebcd116146188e4b', 1);
""")
connection.commit()