import sqlite3

with sqlite3.connect("cookbook.db") as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE recipes(title TEXT, description TEXT)")
    c.execute("INSERT INTO recipes VALUES('Hard Boiled Egg', 'Easy to make hard boiled eggs. Takes only 5 mins.')")
    c.execute("INSERT INTO recipes  VALUES('Spaghetti Bolognese', 'Tasty bolognese with real natural ingredients from scratch')")

