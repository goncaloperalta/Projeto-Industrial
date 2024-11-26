import Database from "better-sqlite3"

const db = new Database('app.db')
db.pragma('journal_mode = WAL')

export const GET = async () => {
    const res = await fetch("http://localhost:8000/start", { signal: AbortSignal.timeout(10000) })
    const data = await res.json()
    
    console.log(data)
    const insertData = db.prepare("INSERT INTO tests (button, success, force_val, time_val, date, time) VALUES (?, ?, ?, ?, ?, ?)");
    insertData.run(data.feedback.button, data.success, JSON.stringify(data.force_val), JSON.stringify(data.time_val), data.date, data.time);

    return new Response(JSON.stringify({data: data}), {status: 201})
}