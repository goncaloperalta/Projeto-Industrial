import Database from "better-sqlite3"

const db = new Database('app.db')
db.pragma('journal_mode = WAL')

const insertData = db.prepare("INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (?, ?, ?, ?, ?, ?)");
insertData.run("WPS", 1, "{0, 1, 2, 3, 4, 5, 6}", "{0, 1, 2, 3, 4, 5, 6}", "2023-10-12", "23:14:53");

