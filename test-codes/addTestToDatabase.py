import sqlite3 as sql
import json
from time import sleep
from datetime import datetime

now = datetime.now()
date = now.strftime("%d-%m-%y")
time = now.strftime("%H:%M:%S")

db = sql.connect("../control-code/app.db")
cur = db.cursor()

data = {
    "force_val": "[",
    "time_val": "[",
}

id = cur.execute(f"INSERT INTO tests (success, force_val, time_val) VALUES (\"[\", \"[\", \"[\")").lastrowid
print(id)
data = [1, 2, 3, 4]
n = 3
for i in range(n):
    setquery = f"{data}"
    if i == 0:
        cur.execute(f"UPDATE tests SET success = success || \"{n}\", force_val = force_val || \"{data}\", time_val = time_val || \"{data}\" WHERE id = {id}")
    elif i == n-1:
        cur.execute("""UPDATE tests SET 
                    success = success || ?,
                    force_val = force_val || ?,
                    time_val = time_val || ?
                    WHERE id = ?""", (f", {n}", f", {data}]", f", {data}]", id))
    else:
        cur.execute(f"UPDATE tests SET success = success || \", {n}\", force_val = force_val || \", {data}\", time_val = time_val || \", {data}\" WHERE id = {id}")

row = cur.execute(f"SELECT * FROM tests WHERE id = {id}").fetchone()
print(row)

cur.execute(f"UPDATE tests SET button = \"WPS\", error = \"No error\", presses = 1, parameters = \"[1, 2, 3]\", date = \"{date}\" WHERE id = {id}")
row = cur.execute(f"SELECT * FROM tests WHERE id = {id}").fetchone()
print(row)
if row[9] == None:
    print("123")
# cur.execute(f"INSERT INTO tests (button, success, error, presses, parameters, force_val, time_val, date, time) VALUES (\"{data['button']}\", \"{data['success']}\", {data['error']}, {data['presses']}, \"{data['parameters']}\", \"{data['force_val']}\", \"{data['time_val']}\", \"{data['date']}\", \"{data['time']}\")")
# row = cur.execute("SELECT id FROM tests ORDER BY id DESC LIMIT 1").fetchone()
# print(row)

db.commit()
cur.close()
db.close()