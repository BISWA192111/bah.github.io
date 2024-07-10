import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('craters.db')
cursor = conn.cursor()

# Create the table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS craters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_x INTEGER,
    image_y INTEGER,
    latitude REAL,
    longitude REAL
)
''')

# Insert dummy data
cursor.execute('INSERT INTO craters (image_x, image_y, latitude, longitude) VALUES (?, ?, ?, ?)', (50, 50, 5.0, 5.0))

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database and table created, and dummy data inserted successfully.")
