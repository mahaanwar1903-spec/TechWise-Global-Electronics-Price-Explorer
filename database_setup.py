import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    store TEXT,
    link TEXT
)
''')

cursor.execute("INSERT INTO products (name, price, store, link) VALUES ('Samsung Galaxy A15', 55000, 'Daraz', 'https://www.daraz.pk')")
cursor.execute("INSERT INTO products (name, price, store, link) VALUES ('HP Laptop 15s', 120000, 'Mega.pk', 'https://www.mega.pk')")
cursor.execute("INSERT INTO products (name, price, store, link) VALUES ('Haier Refrigerator', 75000, 'Homeshopping.pk', 'https://www.homeshopping.pk')")
connection.commit()
connection.close()

print("Database created and sample data added successfully!")
