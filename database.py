import sqlite3

conn = sqlite3.connect('sensors.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT NOT NULL PRIMARY KEY,
    event_type TEXT NOT NULL,
    business_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    payload TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_summary (
    sensor_id INTEGER NOT NULL PRIMARY KEY,
    last_temperature REAL NOT NULL,
    last_humidity REAL NOT NULL,
    last_soil_moisture REAL NOT NULL
)
''')

conn.commit()
conn.close()


