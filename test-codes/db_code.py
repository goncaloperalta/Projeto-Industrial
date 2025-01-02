import sqlite3 as sql
import json
from datetime import datetime


now = datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%H:%M:%S")

db = sql.connect("app.db")
cur = db.cursor()

# data = {
#     "button": "INFO",
#     "success": 1,
#     "force_val": [1, 2, 3, 4, 5],
#     "time_val": [1, 2, 3, 4, 5],
#     "date": date,
#     "time": time
# }

# profile = {
#     "pName": "Reset",
#     "pressTime": 1,
#     "nTimes": 1,
#     "interval": 2
# }

# try:
#     cur.execute(f"INSERT INTO tests (pName, pressTime, nTimes, interval) VALUES (\"{profile['pName']}\", {profile['pressTime']}, {profile['nTimes']}, {profile['interval']})")
# except sql.OperationalError as e:
#     print(e)

# cur.execute(f"INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (\"{data['button']}\", {data['success']}, \"{[data['force_val']]}\", \"{[data['time_val']]}\", \"{data['date']}\", \"{data['time']}\")")
# x = cur.execute(f"SELECT * FROM profiles WHERE pName = \"123\"").fetchone()
# print(x)

db.commit()
cur.close()
db.close()