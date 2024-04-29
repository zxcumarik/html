import sqlite3

# sqlite_connection = sqlite3.connect('test_database_db')
# cursor = sqlite_connection.cursor()
# cursor.execute('''
# ''')
# sqlite_connection.close()

with sqlite3.connect('test_database.db') as sqlite_connection:
    cursor = sqlite_connection.cursor()
    cursor.execute('''CREATE TABLE Users (
    name TEXT,
    age INTEGER,
    class INTEGER,
    city TEXT
     )''')
