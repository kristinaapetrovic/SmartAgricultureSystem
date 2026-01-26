import sqlite3;

conn = sqlite3.connect('sensors.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    bussiness_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    payload TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_summary (
    sensor_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    last_temperature REAL NOT NULL,
    last_humidity REAL NOT NULL,
    last_soil_moisture REAL NOT NULL
)
''')

conn.commit()
conn.close()