import sqlite3 as sql
import json
from datetime import datetime

now = datetime.now()
date = now.strftime("%d-%m-%y")
time = now.strftime("%H:%M:%S")

db = sql.connect("../control-code/app.db")
cur = db.cursor()

data = {
    "button": "INFO",
    "success": [1, 1, 1],
    "error": "123",
    "presses": 2,
    "parameters": [1, 1, 1],
    "force_val": [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
    "time_val": [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
    "date": date,
    "time": time
}

cur.execute(f"INSERT INTO tests (button, success, error, presses, parameters ,force_val, time_val, date, time) VALUES (\"{data['button']}\", \"{data['success']}\", {data['error']}, {data['presses']}, \"{data['parameters']}\", \"{data['force_val']}\", \"{data['time_val']}\", \"{data['date']}\", \"{data['time']}\")")

db.commit()
cur.close()
db.close()