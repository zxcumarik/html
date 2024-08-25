import sqlite3

# sqlite_connection = sqlite3.connect('test_database_db')
# cursor = sqlite_connection.cursor()
# cursor.execute('''
# ''')
# sqlite_connection.close()

with sqlite3.connect('test_database.db') as sqlite_connection:
    cursor = sqlite_connection.cursor()
#     cursor.execute('''CREATE TABLE Users (
#     name TEXT,
#     second_name PRIMARY KEY,
#     class INTEGER,
#     city TEXT
#      )''')

# -- INSERT INTO Users VALUES('Maksim', 'Smuglin', 10, 'Tartu')
# -- INSERT INTO Users VALUES('Arina', 'Albahktina', 11, 'Lviv')
# -- INSERT INTO Users VALUES('Natalia', 'Stroman', 10, 'Tartu')
# -- INSERT INTO Users VALUES('Oleh', 'Hulik', 10, 'Lviv')
# UPDATE Users SET class = class + 1 WHERE class = 10
cursor.execute('''SELECT count(class) as count, class
ROM Users
GROUP BY class</sql><current_tab id="0"/></tab_sql></sqlb_project>''')