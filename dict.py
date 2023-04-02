# # open the text file
# with open('bag_of_words.txt', 'r') as f:
#     # read the text file into a list of lines
#     lines = f.readlines()
#
# # create an empty dictionary
# bag_of_words = {}
#
# # loop through the lines in the text file
# for line in lines:
#     # split the line on ','
#     key, value = line.split(',')
#     # strip the whitespace
#     key = key.strip()
#     value = value.strip()
#     # add the key, value pair to the dictionary
#     bag_of_words[key] = value
#
# # print the dictionary
# print(bag_of_words)


# # Save a dictionary to a text file
# import json
# bag_of_words = {
#     'die Anmerkung': 'simeiosi',
#     'die Auflage': 'stroma',
#     'die Aufklärung': 'eksigisi',
#     'aufschreiben - notieren': 'simeiono',
#     'die Dichtung': 'poiisi',
#     'die Reinheit': 'agnotita',
#     'derentwillen': 'eksaitias tis thelisis tous',
#     'die Neigung - Vorliebe': 'protimisi',
#     'die Poesie': 'poiisi',
#     'umstritten': 'epimaxos',
#     'die Grausamkeit': 'thiriodia'
# }
# print('bag_of_words dictionary')
# print(bag_of_words)
#
# print("Save dictionary to a .txt file")
# with open("bag_of_words.txt", "w") as fp:
#     json.dump(bag_of_words, fp)  # encode dict into JSON
# print("Done writing dict into .txt file")


# # Read a dictionary from a text file.
# import json
# # Open the file for reading
# with open("bag_of_words.txt", "r") as fp:
#     # Load the dictionary from the file
#     bag_of_words = json.load(fp)
# # Print the contents of the dictionary
# print(bag_of_words)



# import pandas as pd
# # Read the Excel file into a pandas DataFrame
# df = pd.read_excel('words.xlsx')
# # Convert the DataFrame into a dictionary
# bag_of_words = dict(zip(df.iloc[:,0], df.iloc[:,1]))
# print(bag_of_words)

import os
# db.sqlite3


# path = os.getcwd() # get current working directory
# if not os.path.exists(path): # check if a path doesn't exists
#     # os.makedirs(path) # true --> create path
#     print("created a folder")
# else:
#     print("you have to create db")

import os, random, sqlite3

# create SQLite database if it doesn't exist
if not os.path.exists("db.sqlite3"):
    # print("Database db.sqlite3 does not exists!")
    conn = sqlite3.connect('db.sqlite3') # db.sqlite3 database.db
    cursor = conn.cursor()
    # create User table
    cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL CHECK(gender in ('Female', 'Male', 'Other')), 
                    age INTEGER NOT NULL,
                    date_signup DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()