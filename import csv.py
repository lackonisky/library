import array
import csv
import pandas as pd
import random
#import the sqlite3 library so it can be used to interact with the database
import sqlite3
# connects to the database and creates one if one is not already present
connection = sqlite3.connect("library5.db")
# a database cursor is created so it can be used to execute SQL commands
cursor = connection.cursor()
data = pd.read_csv("https://data.seattle.gov/resource/6vkj-f5xf.csv?$query=SELECT%0A%20%20%60bibnum%60%2C%0A%20%20%60title%60%2C%0A%20%20%60author%60%2C%0A%20%20%60isbn%60%2C%0A%20%20%60publicationyear%60%2C%0A%20%20%60publisher%60%2C%0A%20%20%60subjects%60%2C%0A%20%20%60itemtype%60%2C%0A%20%20%60itemcollection%60%2C%0A%20%20%60floatingitem%60%2C%0A%20%20%60itemlocation%60%2C%0A%20%20%60reportdate%60%2C%0A%20%20%60itemcount%60%0AORDER%20BY%20%60reportdate%60%20ASC%20NULL%20LAST")
data = data.to_numpy()
print(len(data))
for n in range(len(data)):
    if n%10000 ==0 :
        print(data[n][0])
    cursor.execute("""INSERT INTO Books (ISBN, AUTHOR, TITLE, DATEPUBLISHED, FORMAT, STOCK, DESCRIPTION)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (data[n][1], data[n][2], data[n][3], data[n][4], data[n][5], random.randint(1,5), data[n][6],))
connection.commit()
