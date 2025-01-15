import sqlite3 as sql
from datetime import datetime

now = datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S")

db = sql.connect("app.db")
cur = db.cursor()

cur.execute("""CREATE TABLE tests(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                button      VARCHAR(255),
                success     TEXT,
                error       VARCHAR(255),
                presses     INT,
                parameters  TEXT,
                force_val   TEXT,
                time_val    TEXT,
                date        DATE,
                time        TIME
            )""")

cur.execute("""CREATE TABLE profiles (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                pName       VARCHAR(255) UNIQUE,
                pressTime   INT,
                nTimes      INT,
                interval    INT
            )""")

cur.execute("""INSERT INTO profiles (pName, pressTime, nTimes, interval) VALUES (
                    "Custom", 0, 1, 0
                )""")

cur.execute("""INSERT INTO tests (button, success, error, presses, parameters, force_val, time_val, date, time) VALUES (
                "None",
                "[1]",
                "No Error",
                1,
                "[0, 1, 0]",
                "[1, 2, 3]",
                "[1, 2, 3]",
                "15-01-2025",
                "15:01:22"
)""")
#     cur.execute(f"INSERT INTO tests 
# (pName, pressTime, nTimes, interval) 
# VALUES (\"{profile['pName']}\", {profile['pressTime']}, {profile['nTimes']}, {profile['interval']})")

db.commit()
cur.close()
db.close()
